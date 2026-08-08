# -*- coding: utf-8 -*-

import logging
import re
from datetime import datetime

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

try:
    import feedparser
except ImportError:
    feedparser = None


class ChurchNewsSource(models.Model):
    _name = 'church.news.source'
    _description = 'News Source'

    name = fields.Char(string='Name', required=True)
    url = fields.Char(string='Website URL')
    rss_feed_url = fields.Char(string='RSS Feed URL', required=True)
    active = fields.Boolean(string='Active', default=True)

    @api.model
    def fetch_daily_news(self):
        """Fetch the 5 most recent, non-duplicated articles from all active sources."""
        if feedparser is None:
            _logger.error(
                'feedparser is not installed. Add it to requirements.txt '
                'and install it to fetch news.'
            )
            return 0

        created_count = 0
        article_model = self.env['church.news.article']
        sources = self.search([('active', '=', True)])

        for source in sources:
            if not source.rss_feed_url:
                continue
            try:
                feed = feedparser.parse(source.rss_feed_url)
            except Exception as e:
                _logger.warning(
                    'Failed to parse RSS feed %s for source %s: %s',
                    source.rss_feed_url, source.name, e,
                )
                continue

            for entry in feed.entries[:5]:
                title = entry.get('title', '').strip()
                link = entry.get('link', '').strip()
                if not title or not link:
                    continue

                summary = entry.get('summary') or entry.get('description') or ''

                published_dt = None
                published_parsed = entry.get('published_parsed') or entry.get('updated_parsed')
                if published_parsed:
                    try:
                        published_dt = datetime(*published_parsed[:6])
                    except Exception:
                        published_dt = None

                # Deduplication: skip if an article with this unique_hash already exists.
                if article_model.search_count([('unique_hash', '=', link)]):
                    continue

                # Auto-categorize from title + summary via keyword matching.
                text = title
                if summary:
                    text += ' ' + re.sub(r'<[^>]+>', ' ', summary)
                categories = self.env['church.news.category'].match_articles(text)

                article_model.create({
                    'title': title,
                    'summary': summary,
                    'published_date': published_dt,
                    'source_id': source.id,
                    'original_url': link,
                    'unique_hash': link,
                    'category_ids': [(6, 0, categories.ids)],
                })
                created_count += 1

        _logger.info('Fetch daily news completed. Created %d new articles.', created_count)
        return created_count
