import datetime
import os
import re

from django.utils.html import strip_tags
from lxml import etree
from pytz import UTC

from exchange import models
from exchange.choices import StackExchangeSiteChoices


BATCH_SIZE = 500


def parse_date(dt):
    if dt:
        return datetime.datetime.fromisoformat(dt).replace(tzinfo=UTC)


def import_posts(source_site, path):
    assert source_site in dict(StackExchangeSiteChoices.choices)

    posts_path = os.path.join(path, 'Posts.xml')
    already_parsed_qs = models.StackExchangePost.objects.values_list(
        'source_site', 'source_id', 'id'
    ).iterator()
    posts_cache = {(x[0], x[1]): x[2] for x in already_parsed_qs}

    i = 0
    for _, row in etree.iterparse(posts_path, tag='row'):
        i += 1
        source_id = int(row.get('Id'))
        body = row.get('Body').strip()
        body_cleaned = strip_tags(body).replace('\n', '').replace('\t', ' ')
        body_cleaned = re.sub(' +', ' ', body_cleaned)
        data = {
            'source_type': int(row.get('PostTypeId')),
            'source_parent_id': int(row.get('ParentId'))
            if row.get('ParentId') else None,
            'score': int(row.get('Score')),
            'body': body,
            'body_cleaned': body_cleaned,
            'owner_user_id': int(row.get('OwnerUserId'))
            if row.get('OwnerUserId') else None,
            'source_created': parse_date(row.get('CreationDate')),
            'source_activity_date': parse_date(row.get('LastActivityDate')),
            'comments_count': int(row.get('CommentCount', 0))
        }
        if data['source_parent_id']:
            data['parent_id'] = posts_cache.get(
                (source_site, data['source_parent_id'])
            )

        if i % 100 == 0:
            print(f'{i}) {source_id}: {body_cleaned[:50]}')

        if (source_site, source_id) in posts_cache:
            post_id = posts_cache[(source_site, source_id)]
            models.StackExchangePost.objects.filter(id=post_id).update(**data)
        else:
            obj = models.StackExchangePost.objects.create(
                source_site=source_site,
                source_id=source_id,
                **data
            )
            posts_cache[(source_site, source_id)] = obj.id

        row.clear()
