import os
from datetime import date
from xml.etree import ElementTree

from flask_frozen import Freezer

from app import app

BASE_URL = "https://www.danhartropp.com"

# The eleven aphorisms lived at /read/*.html until they moved to /code/*.html.
# This list is deliberately frozen rather than derived from the content folder:
# deriving it would mint a redirect for every future /code/ post, and one of
# those could later hijack a genuine /read/ article that shares its slug.
LEGACY_READ_SLUGS = [
    'YAGNI',
    'building_a_team',
    'certification_and_data',
    'code_review',
    'customers_and_requirements',
    'documentation',
    'grugbrain',
    'make_one_to_throw_away',
    'refactor_for_simplicity',
    'testing_and_load_testing',
    'when_things_go_wrong',
]

# feed.xml is served as application/rss+xml; the .xml extension makes
# Frozen-Flask warn about a mismatch it does not need to care about.
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True

freezer = Freezer(app)


def slugs(name):
    """Post slugs in a section, ignoring its index.md."""
    directory = os.path.join('content', name)
    return [f[:-3] for f in sorted(os.listdir(directory))
            if f.endswith('.md') and f != 'index.md']


# The index and feed routes take no arguments, so Frozen-Flask finds them by
# itself. Only the post routes need to be told what exists.
@freezer.register_generator
def read_post():
    for slug in slugs('read'):
        yield {'slug': slug}


@freezer.register_generator
def code_post():
    for slug in slugs('code'):
        yield {'slug': slug}


def write_redirects():
    """Netlify _redirects, served from the publish root."""
    lines = ["# Aphorisms moved from /read/ to /code/ when /read/ became the AI section."]
    for slug in LEGACY_READ_SLUGS:
        lines.append("/read/%s.html  /code/%s.html  301" % (slug, slug))
    with open('build/_redirects', 'w') as handle:
        handle.write("\n".join(lines) + "\n")
    return len(LEGACY_READ_SLUGS)


def write_sitemap(urls):
    urlset = ElementTree.Element('urlset')
    urlset.attrib['xmlns'] = "http://www.sitemaps.org/schemas/sitemap/0.9"

    today = date.today().isoformat()
    count = 0
    for url in sorted(urls):
        if url.startswith('/static') or not url.endswith('.html'):
            continue
        element = ElementTree.SubElement(urlset, 'url')
        ElementTree.SubElement(element, 'loc').text = BASE_URL + url
        ElementTree.SubElement(element, 'lastmod').text = today
        ElementTree.SubElement(element, 'changefreq').text = 'monthly'
        # index pages turn over more often than individual pieces
        ElementTree.SubElement(element, 'priority').text = (
            '1.0' if url.endswith('/index.html') else '0.8')
        count += 1

    ElementTree.ElementTree(urlset).write(
        'build/sitemap.xml', encoding='utf-8', xml_declaration=True)
    return count


if __name__ == '__main__':
    # Generates the static site in 'build', plus sitemap.xml and _redirects.
    frozen = [url.url for url in freezer.freeze_yield()]
    pages = write_sitemap(frozen)
    redirects = write_redirects()
    print("froze %d urls, %d in sitemap, %d redirects" % (len(frozen), pages, redirects))
