# -*- coding: utf-8 -*-

from collections import OrderedDict


class Sidebar(object):

    categories = OrderedDict([
        (
            'selected', dict(
                hr='odabrani radovi',
                eng='selected works'
            )
        ),
        (
            'drafts', dict(
                hr='ostalo / skice',
                eng='other / drafts'
            )
        )
    ])

    def __init__(self, pages, active_path, lang):
        sorted_pages = sorted(pages, reverse=True,
                              key=lambda p: p.meta['date'])

        sidebar_categories = OrderedDict((
            (key, {
                'key': key,
                'projects': [],
                'title': self.categories.get(key).get(lang)
            }) for key in self.categories.keys()
        )
        )

        for page in sorted_pages:
            if not page.meta.get('hide'):
                sidebar_categories.get(page.meta.get('category')).get('projects').append({
                    'title': page.meta.get('title'),
                    'path': page.path,
                    'active': page.path == active_path
                })

        for group in sidebar_categories.values():
            group['has_active_project'] = any([
                p['active'] for p in group['projects']
            ])

        self.sidebar_categories = sidebar_categories
