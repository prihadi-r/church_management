# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ChurchNewsCategory(models.Model):
    _name = 'church.news.category'
    _description = 'News Category'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    slug = fields.Char(string='Slug', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    color = fields.Integer(string='Color Index', default=0)
    keywords = fields.Text(
        string='Keywords',
        help='Comma-separated keywords used to auto-categorize articles. '
             'An article is assigned to this category when any keyword '
             'appears in its title or summary (case-insensitive).',
    )
    active = fields.Boolean(string='Active', default=True)

    article_ids = fields.Many2many(
        'church.news.article',
        'church_news_article_category_rel',
        'category_id',
        'article_id',
        string='Articles',
    )

    @api.model
    def match_articles(self, text):
        """Return the active categories whose keywords appear in ``text``.

        If no category matches, fall back to the category with slug
        ``general`` (so every article ends up categorized).
        """
        Category = self.env['church.news.category']
        lowered = (text or '').lower()
        matched = Category
        for cat in Category.search([('active', '=', True)]):
            if not cat.keywords:
                continue
            for kw in cat.keywords.split(','):
                kw = kw.strip().lower()
                if len(kw) >= 3 and kw in lowered:
                    matched |= cat
                    break
        if not matched:
            general = Category.search([('slug', '=', 'general')], limit=1)
            if general:
                matched = general
        return matched
