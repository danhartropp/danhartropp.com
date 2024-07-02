from flask_frozen import Freezer
from app import app
from xml.etree import ElementTree
from datetime import datetime

BASE_URL = "https://www.danhartropp.com"

freezer = Freezer(app)

if __name__ == '__main__':

    # This generates the static files in 'build' and sitemap.xml
    # The magic is done by using url_for() in the Flask routes

    urlset = ElementTree.Element('urlset')
    urlset.attrib['xmlns']="http://www.sitemaps.org/schemas/sitemap/0.9"

    now = datetime.now().date().isoformat()
    for url in freezer.freeze_yield():
        if not url.url.startswith('/static'):
            el = ElementTree.SubElement(urlset, 'url')
            ElementTree.SubElement(el, 'loc').text = BASE_URL + url.url
            ElementTree.SubElement(el, "lastmod").text = now
            ElementTree.SubElement(el, "changefreq").text = "weekly"
            ElementTree.SubElement(el, "priority").text = "1.0"
    
    tree = ElementTree.ElementTree(urlset)
    tree.write('build/sitemap.xml', encoding='utf-8', xml_declaration=True)