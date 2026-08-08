# -*- coding: utf-8 -*-

import re

from odoo import fields, models


class ChurchNewsArticle(models.Model):
    _name = 'church.news.article'
    _description = 'News Article'
    _order = 'published_date desc'

    title = fields.Char(string='Title', required=True)
    summary = fields.Html(string='Summary')
    published_date = fields.Datetime(string='Published Date')
    source_id = fields.Many2one(
        'church.news.source',
        string='Source',
        required=True,
        ondelete='cascade',
    )
    original_url = fields.Char(string='Original URL', required=True)
    unique_hash = fields.Char(
        string='URL/Hash for Deduplication',
        index=True,
    )
    category_ids = fields.Many2many(
        'church.news.category',
        'church_news_article_category_rel',
        'article_id',
        'category_id',
        string='Categories',
    )

    _sql_constraints = [
        ('unique_hash_uniq', 'UNIQUE(unique_hash)',
         'An article with this URL/hash already exists.'),
    ]

    def recategorize(self):
        """Re-run keyword auto-categorization on the given articles."""
        category_model = self.env['church.news.category']
        for art in self:
            text = art.title or ''
            if art.summary:
                text += ' ' + re.sub(r'<[^>]+>', ' ', art.summary)
            art.category_ids = category_model.match_articles(text)
        return True
