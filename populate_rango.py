import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django

django.setup()

from rango.models import Category, Page


def populate():
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url': "http://docs.python.org/2/tutorial/",
         'content': "你是世界上最好的人",
         'views_page': 128},
        {'title': 'How to Think like a Computer Scientist',
         'url': "http://www.greenteapress.com/thinkpython/",
         'views_page': 64},
        {'title': 'Learn Python in 10 Minutes',
         'url': "http://www.korokithakis.net/tutorials/python/",
         'views_page': 32},
    ]

    django_pages = [
        {"title": "Official Django Tutorial",
         "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
         'views_page': 64},
        {"title": "Django Rocks",
         "url": "http://www.djangorocks.com/",
         'views_page': 32},
        {"title": "How to Tango with Django",
         "url": "http://www.tangowithdjango.com/",
         'views_page': 16},
    ]
    other_pages = [
        {"title": "Bottle",
         "url": "http://bottlepy.org/docs/dev/",
         'views_page': 32},
        {"title": "Flask",
         "url": "http://flask.pocoo.org",
         'views_page': 16}, ]

    cats = {
        'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
        'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
        'Other': {'pages': other_pages, 'views': 32, 'likes': 16},
    }

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['content'], p['views_page'])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


def add_page(cat, title, url, content, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    print(p)
    p.url = url
    p.views = views
    p.save()
    return p


if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
