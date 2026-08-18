import os
from datetime import date, datetime

from flask import Flask, render_template, url_for, Response
import frontmatter
import markdown

app = Flask(__name__, static_folder='static')

SITE_URL = 'https://www.danhartropp.com'
SITE_TITLE = 'Dan Hartropp'
SITE_TAGLINE = 'Tech pragmatist, sometime startup CTO and once-upon-a-time digital artist.'

# Every writing section on the site. Adding one is a folder in content/ plus an
# entry here; the index page, RSS feed and sitemap entries all follow from it.
COLLECTIONS = {
    'read': {
        'nav': 'read',
        'heading': 'Applied AI',
        'strapline': 'Notes from actually building the things',
        'description': 'Writing about applied AI — what works, what does not, '
                       'and what it costs to find out.',
        'intro': 'Practical notes on building with AI: what held up in production, '
                 'what quietly fell over, and the bits nobody puts in the demo.',
        'empty': 'Nothing published here yet. The first pieces are on their way — '
                 'the feed is live if you would rather be told than remember to check.',
    },
    'code': {
        'nav': 'code',
        'heading': 'Some thoughts',
        'strapline': 'In no particular order',
        'description': "Some tech and startup lessons I've learned the hard way over the years.",
        'intro': 'Some thoughts loosely based on the theme of technical management in a '
                 "startup environment. Don't take any of this as hard-and-fast advice — "
                 "it's based on my personal experience and comes with the caveats that implies.",
        'empty': 'Nothing here yet.',
    },
}

# Restrict the collection placeholder so these routes can never shadow /look/.
COLLECTION_RULE = '<any(%s):collection>' % ','.join(COLLECTIONS)


def _absolute(path):
    return SITE_URL + path


def get_posts(collection):
    """Load, render and date-sort every post in a collection."""
    directory = os.path.join('content', collection)
    posts = []
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith('.md'):
            continue
        post = frontmatter.load(os.path.join(directory, filename))
        post['slug'] = filename[:-3]
        post['url'] = url_for('post', collection=collection, slug=post['slug'])
        post.content = markdown.markdown(post.content)
        if 'excerpt' not in post.keys():
            post['excerpt'] = post.content.split('\n')[0]
        posts.append(post)

    today = date.today()  # handle missing dates in the sort
    posts.sort(key=lambda p: p['date'] or today, reverse=True)
    return posts


def get_arts(path):
    art_files = sorted(os.listdir('content/look/' + path))
    art_files = [x for x in art_files if x.endswith('.md') and x != 'index.md']
    arts = [frontmatter.load('content/look/' + path + '/' + art) for art in art_files]
    for idx, art in enumerate(arts):
        art['url'] = url_for('art', path=path + '/' + art_files[idx].replace('.md', '.html'))
    return arts


@app.template_filter('rfc822')
def rfc822(value):
    """RSS pubDate wants RFC 822; frontmatter gives us a date or datetime."""
    if not value:
        return ''
    if not isinstance(value, datetime):
        value = datetime(value.year, value.month, value.day)
    return value.strftime('%a, %d %b %Y %H:%M:%S +0000')


@app.template_filter('longdate')
def longdate(value):
    return value.strftime('%d %B %Y') if value else ''


@app.context_processor
def globals():
    return {
        'collections': COLLECTIONS,
        'site_title': SITE_TITLE,
        'site_tagline': SITE_TAGLINE,
        'site_url': SITE_URL,
        'year': date.today().year,
    }


@app.route('/index.html')
def index():
    return render_template('index.html', section='home', canonical='/index.html')


@app.route('/contact.html')
def contact():
    return render_template('contact.html', section='contact', canonical='/contact.html')


@app.route('/%s/index.html' % COLLECTION_RULE)
def collection_index(collection):
    return render_template(
        'collection.html',
        section=collection,
        meta=COLLECTIONS[collection],
        posts=get_posts(collection),
        canonical=url_for('collection_index', collection=collection),
    )


@app.route('/%s/feed.xml' % COLLECTION_RULE)
def collection_feed(collection):
    xml = render_template(
        'feed.xml',
        collection=collection,
        meta=COLLECTIONS[collection],
        posts=get_posts(collection)[:20],
        absolute=_absolute,
    )
    return Response(xml, mimetype='application/rss+xml')


@app.route('/%s/<slug>.html' % COLLECTION_RULE)
def post(collection, slug):
    post = frontmatter.load(os.path.join('content', collection, slug + '.md'))
    post.content = markdown.markdown(post.content)
    return render_template(
        'post.html',
        section=collection,
        meta=COLLECTIONS[collection],
        collection=collection,
        post=post,
        canonical=url_for('post', collection=collection, slug=slug),
    )


@app.route('/look/index.html')
def look_index():
    return render_template('look.html', section='look', canonical='/look/index.html')


@app.route('/look/<path:path>')
def art(path):
    # first check whether we want an index page
    if path.split('/')[-1] == 'index.html':
        arts = get_arts(path.split('/')[0])
        series = frontmatter.load('content/look/' + path.replace('.html', '.md'))
        series.content = markdown.markdown(series.content)
        return render_template('look_series.html', section='look', series=series,
                               arts=arts, canonical=url_for('art', path=path))

    # Or whether we're looking for an individual piece page
    art = frontmatter.load('content/look/' + path.replace('.html', '.md'))
    art.content = markdown.markdown(art.content)
    return render_template('art.html', section='look', art=art,
                           canonical=url_for('art', path=path))


@app.route('/robots.txt')
def robots_txt():
    return render_template('robots.txt'), 200, {'Content-Type': 'text/plain; charset=utf-8'}
