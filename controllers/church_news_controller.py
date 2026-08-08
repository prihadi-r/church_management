# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class ChristianityNews(http.Controller):

    @http.route('/christianity-news', type='http', auth='public', website=True)
    def christianity_news(self, **kw):
        Category = request.env['church.news.category'].sudo()
        Article = request.env['church.news.article'].sudo()

        categories = Category.search([('active', '=', True)], order='sequence, name')

        # Optional filter: /christianity-news?category=<slug>
        active_category = Category
        category_slug = (kw.get('category') or '').strip()
        if category_slug and category_slug != 'all':
            active_category = Category.search([('slug', '=', category_slug)], limit=1)

        if active_category:
            # Filtered view: flat grid of the selected category's articles.
            articles = Article.search(
                [('category_ids', 'in', active_category.id)],
                order='published_date desc', limit=100,
            )
            groups = []
        else:
            # Overview view: every article, grouped by category.
            articles = Article.search([], order='published_date desc', limit=200)
            groups = []
            for cat in categories:
                cat_articles = articles.filtered(lambda a: cat in a.category_ids)
                if cat_articles:
                    groups.append({
                        'category': cat,
                        'articles': cat_articles,
                    })

        return request.render('church_management.news_page', {
            'articles': articles,
            'categories': categories,
            'active_category': active_category,
            'groups': groups,
        })
