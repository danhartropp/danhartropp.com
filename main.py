import os
from flask import Flask, render_template, url_for
import frontmatter
import markdown

app = Flask(__name__, static_folder='static')

def get_posts():
    posts = os.listdir('content/read/')
    parsed_posts = []
    for post in posts:
        parsed_post = frontmatter.load('content/read/' + post)
        parsed_post['url'] = url_for('post', path=post.replace('.md',''))
        if 'excerpt' not in parsed_post.keys():
            parsed_post.excerpt = parsed_post.content.split('\n')[0]
        parsed_posts.append(parsed_post)
    parsed_posts.sort(key = lambda x: x['date'], reverse=True)
    return parsed_posts

def get_arts(path):
    print (path)
    art_files = os.listdir('content/look/' + path)
    arts = [frontmatter.load('content/look/' + path + '/' + art) for art in art_files]
    for idx, art in enumerate(arts):
        art['url'] = url_for('art', path=path + '/' + art_files[idx].replace('.md',''))
    return arts

@app.route('/')
def index():
    featured_posts = get_posts()[:2]
    return render_template('index.html', featured_posts=featured_posts)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/read')
def read_index():
    posts = get_posts()
    return render_template('read.html',posts=parsed_posts)

@app.route('/read/<path:path>')
def post(path):
    post = frontmatter.load('content/read/' + path + '.md')
    post.content = markdown.markdown(post.content)
    return render_template('post.html',post=post)

@app.route('/look/<path:path>')
def art(path):

    #first check whether we want an index page 
    if len(path.split('/')) == 1:
        arts = get_arts(path.replace('/',''))
        return render_template('look.html', arts=arts)

    #Or whether we're looking for an individual piece page
    art = frontmatter.load('content/look/' + path + '.md')
    art.content = markdown.markdown(art.content)
    return render_template('art.html',art=art)

