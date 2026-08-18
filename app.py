import os
from datetime import date, datetime

from flask import Flask, render_template, url_for, Response
import frontmatter
import markdown

app = Flask(__name__, static_folder='static')

SITE_URL = 'https://www.danhartropp.com'
SITE_TITLE = 'Dan Hartropp'
SITE_TAGLINE = 'Tech pragmatist, sometime startup CTO and once-upon-a-time digital artist.'


def load_section(name):
    """A section's heading and intro live in content/<name>/index.md."""
    section = frontmatter.load(os.path.join('content', name, 'index.md'))
    section.content = markdown.markdown(section.content)
    return section


def get_posts(name):
    """Load, render and date-sort every post in a section."""
    directory = os.path.join('content', name)
    posts = []
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith('.md') or filename == 'index.md':
            continue
        post = frontmatter.load(os.path.join(directory, filename))
        post['section'] = name
        post['url'] = '/%s/%s.html' % (name, filename[:-3])
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


def render_index(name):
    return render_template('collection.html', section=name, meta=load_section(name),
                           posts=get_posts(name),
                           canonical='/%s/index.html' % name)


def all_posts():
    """Every post from every section, newest first."""
    posts = get_posts('read') + get_posts('code')
    today = date.today()
    posts.sort(key=lambda p: p['date'] or today, reverse=True)
    return posts


def render_post(name, slug):
    post = frontmatter.load(os.path.join('content', name, slug + '.md'))
    post.content = markdown.markdown(post.content)
    return render_template('post.html', section=name, meta=load_section(name),
                           post=post,
                           canonical='/%s/%s.html' % (name, slug))


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


@app.route('/feed.xml')
def feed():
    xml = render_template('feed.xml', posts=all_posts()[:20])
    return Response(xml, mimetype='application/rss+xml')


@app.route('/read/index.html')
def read_index():
    return render_index('read')


@app.route('/read/<slug>.html')
def read_post(slug):
    return render_post('read', slug)


@app.route('/code/index.html')
def code_index():
    return render_index('code')


@app.route('/code/<slug>.html')
def code_post(slug):
    return render_post('code', slug)


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
