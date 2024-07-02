import os
from flask import Flask, render_template, url_for, redirect
import frontmatter
import markdown
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True

def get_posts():
    posts = os.listdir('content/read/')
    parsed_posts = []
    for post in posts:
        parsed_post = frontmatter.load('content/read/' + post)
        parsed_post['url'] = url_for('post', path=post.replace('.md','.html'))
        parsed_post.content = markdown.markdown(parsed_post.content)
        if 'excerpt' not in parsed_post.keys():
            parsed_post['excerpt'] = parsed_post.content.split('\n')[0]
        parsed_posts.append(parsed_post)
    
    today = datetime.now().date() # handle missing dates in the sort
    parsed_posts.sort(key = lambda x: x['date'] or today, reverse=True)
    return parsed_posts

def get_arts(path):
    art_files = os.listdir('content/look/' + path)
    art_files = [x for x in art_files if x != 'index.md']
    arts = [frontmatter.load('content/look/' + path + '/' + art) for art in art_files]
    for idx, art in enumerate(arts):
        art['url'] = url_for('art', path=path + '/' + art_files[idx].replace('.md','.html'))
    return arts

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/read/index.html')
def read_index():
    posts = get_posts()
    return render_template('read.html',posts=posts)

@app.route('/read/<path:path>')
def post(path):
    post = frontmatter.load('content/read/' + path.replace('.html','.md'))
    post.content = markdown.markdown(post.content)
    return render_template('post.html',post=post)

@app.route('/look/index.html')
def look_index():
    return render_template('look.html')

@app.route('/look/<path:path>')
def art(path):

    #first check whether we want an index page 
    if path.split('/')[-1] == 'index.html':
        arts = get_arts(path.split('/')[0])
        series = frontmatter.load('content/look/' + path.replace('.html','.md'))
        series.content = markdown.markdown(series.content)
        return render_template('look_series.html', series=series, arts=arts)

    #Or whether we're looking for an individual piece page
    art = frontmatter.load('content/look/' + path.replace('.html','.md'))
    art.content = markdown.markdown(art.content)
    return render_template('art.html',art=art)

@app.route("/robots.txt")
def robots_txt():
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /contact*',
        'Sitemap: https://www.danhartropp.com/sitemap.xml'
    ]
    return '\n'.join(lines), 200, {'Content-Type': 'text/plain; charset=utf-8'}


