# -*- coding: utf-8 -*-

from collections import OrderedDict

class Sidebar(object):

	categories = OrderedDict([
		(
			'selected', dict(
				hr = 'ODABRANI RADOVI',
				eng = 'SELECTED WORKS'
			)
		),
		(
			'collaboration', dict(
				hr = 'SURADNJE',
				eng = 'COLLABORATIONS'
			)
		)
	])

	def __init__(self, pages, active_path, lang):
		sorted_pages = sorted(pages, reverse=True,
                    key=lambda p: p.meta['date'])

		sidebar_categories = OrderedDict((
				(key, {
					'projects': [],
					'title': self.categories.get(key).get(lang)
					}) for key in self.categories.iterkeys()
			)
		)

		for page in sorted_pages:
			if not page.meta.get('hide'):
				sidebar_categories.get(page.meta.get('category')).get('projects').append({
					'title': page.meta.get('title'),
					'path': page.path,
					'active': page.path == active_path
					})

		self.sidebar_categories = sidebar_categories
