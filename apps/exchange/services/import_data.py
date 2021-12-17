import datetime
import os
import re

from django.utils.html import strip_tags
from exchange import models
from exchange.choices import StackExchangeSiteChoices
from lxml import etree
from pytz import UTC

BATCH_SIZE = 500
multi_spaces_match = re.compile(r' +')
multi_lines_match = re.compile(r'\n{2,}')


def parse_date(dt):
    if dt:
        return datetime.datetime.fromisoformat(dt).replace(tzinfo=UTC)


def clean_text(value, join=False):
    # убираем теги и табуляцию
    value = strip_tags(value).replace('\t', ' ')
    # склеиваем пробелы
    value = multi_spaces_match.sub(' ', value)
    # убираем избыточность пустых строк
    value = multi_lines_match.sub('\n', value)
    if join:
        value = value.replace('\n', '')
    return value.strip()


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
        source_type = int(row.get('PostTypeId'))

        title = row.get('Title').strip() if row.get('Title') else ''
        title_cleaned = clean_text(title, join=True) if title else ''

        body = row.get('Body').strip()
        body_cleaned = clean_text(body)

        if i % 100 == 0:
            body_print = body_cleaned[:50].replace("\n", " ")
            print(
                f'{(str(i) + ")").ljust(12)}'
                f'{str(source_id).ljust(12)} '
                f'{source_type}: '
                f'{(title_cleaned[:50] or "-").ljust(50)} '
                f'{body_print}'
            )

        data = {
            'source_type': source_type,
            'source_parent_id': int(row.get('ParentId'))
            if row.get('ParentId') else None,
            'score': int(row.get('Score')),
            'title': title,
            'title_cleaned': title_cleaned,
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

    print('Done')
