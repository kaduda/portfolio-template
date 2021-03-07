# -*- coding: utf-8 -*-

import sys
import os

from flask import Flask, render_template, send_from_directory, url_for
from flask_frozen import Freezer
from flask_flatpages import FlatPages
from PIL import Image

from utils.image import cropped_thumbnail
from utils.sidebar import Sidebar

app = Flask(__name__)
app.config.from_object('config')

freezer = Freezer(app)
hr_pages = FlatPages(app, name='hr')
eng_pages = FlatPages(app, name='eng')

drafts_pages = FlatPages(app, name='drafts')

bio_pages = FlatPages(app, name='bio')


def get_other_lang(lang):
    return 'eng' if lang == 'hr' else 'hr'


def get_pages(lang, reverse=False):
    return hr_pages if lang == 'hr' else eng_pages


def get_translate_url(page, lang):
    new_lang = get_other_lang(lang)
    translated_pages = get_pages(new_lang)

    translated_page = None
    for trans_page in translated_pages:
        if trans_page.meta.get('key') == page.meta.get('key'):
            translated_page = trans_page
            break

    return url_for('project', path=translated_page.path, lang=new_lang)


@app.route('/', defaults=dict(lang='hr'))
@app.route('/eng/', defaults=dict(lang='eng'))
def index(lang):

    pages = get_pages(lang)

    sorted_pages = sorted(pages, reverse=True,
            key=lambda p: p.meta['date'])

    sidebar = Sidebar(pages, '', lang)
    return render_template('home.html',
        sidebar=sidebar,
        pages=sorted_pages,
        lang=lang,
        title='Katerina Duda',
        translate_url=url_for('index', lang=get_other_lang(lang)))


@app.route('/radovi/<category>/', defaults=dict(lang='hr'))
@app.route('/eng/works/<category>/', defaults=dict(lang='eng'))
def category(lang, category):

    pages = get_pages(lang)

    sorted_pages = sorted(pages, reverse=True,
            key=lambda p: p.meta['date'])

    sidebar = Sidebar(pages, '', lang)
    return render_template('category.html',
        sidebar=sidebar,
        pages=sorted_pages,
        lang=lang,
        title='Katerina Duda',
        category=category,
        translate_url=url_for('index', lang=get_other_lang(lang)))


@app.route('/projekti/<path:path>/', defaults=dict(lang='hr'))
@app.route('/eng/projects/<path:path>/', defaults=dict(lang='eng'))
def project(path, lang):
    pages = get_pages(lang)
    page = pages.get(path)

    translate_url = get_translate_url(page, lang)

    sidebar = Sidebar(pages, path, lang)
    return render_template('project.html',
        sidebar=sidebar,
        project=page,
        title=page['title'],
        lang=lang,
        translate_url=translate_url)


@app.route('/bio/', defaults=dict(lang='hr'))
@app.route('/eng/bio/', defaults=dict(lang='eng'))
def bio(lang):
    pages = get_pages(lang)
    bio = bio_pages.get("bio-{}".format(lang))

    translate_url = url_for('bio', lang=get_other_lang(lang))

    sidebar = Sidebar(pages, '', lang)
    return render_template('bio.html',
        sidebar=sidebar,
        bio=bio,
        title=bio['title'],
        lang=lang,
        translate_url=translate_url)


@app.route('/static/thumb/<size>/<path:filename>')
def thumb(size, filename):

    # filename = filename.replace("/", "\\")

    infile = os.path.join('static', filename)
    size = [int(dim) for dim in size.split('x')]

    outfile = list(os.path.split(infile))
    thumb_dir = os.path.join(outfile[0], 'thumb')

    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)

    outfile = os.path.join(thumb_dir, outfile[1])
    im = Image.open(infile)
    output = cropped_thumbnail(im, size)
    output.save(outfile, 'JPEG')

    return send_from_directory(*os.path.split(outfile))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':

        def home_urls():
            return (
                ('index', dict(lang='hr')), ('index', dict(lang='eng')),
                ('category', dict(category='selected', lang='hr')), ('category', dict(category='selected', lang='eng')),
                ('category', dict(category='drafts', lang='hr')), ('category', dict(category='drafts', lang='eng')),

                ('thumb', dict(size='805x463', filename='img/hvala/f-d-1.jpg')),
                ('thumb', dict(size='805x463', filename='img/hvala/f-1.jpg')),
                ('thumb', dict(size='805x463', filename='img/hvala/p-1.jpg')),
                ('thumb', dict(size='805x463', filename='img/hvala/p-3.jpg')),
                ('thumb', dict(size='805x463', filename='img/hvala/f-d-1-1.jpg')),
                ('thumb', dict(size='805x463', filename='img/hvala/f-d-3.jpg')),
                ('thumb', dict(size='805x463', filename='img/hvala/d-1.jpg')),
                ('thumb', dict(size='463x805', filename='img/hvala/k-1.jpg')),
                ('thumb', dict(size='805x463', filename='img/hvala/a-a-1.jpg')),
                ('thumb', dict(size='805x463', filename='img/hvala/a-a-2.jpg')),
                ('thumb', dict(size='805x463', filename='img/hvala/a-1.jpg')),
                ('thumb', dict(size='805x463', filename='img/hvala/f-a-2.jpg')),
                ('thumb', dict(size='805x463', filename='img/hvala/o-1.jpg')),
                ('thumb', dict(size='805x463', filename='img/hvala/o-2.jpg')),
                ('thumb', dict(size='805x463', filename='img/hvala/o-3.jpg')),
                ('thumb', dict(size='805x463', filename='img/hvala/o-4.jpg')),
                ('thumb', dict(size='805x463', filename='img/strujanja/6.jpg')),
                ('thumb', dict(size='805x463', filename='img/fundus/10.jpg')),

            )

        freezer.register_generator(home_urls)
        freezer.freeze()

    else:
        app.run(host='0.0.0.0')
