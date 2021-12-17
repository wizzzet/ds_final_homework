import csv
import os

from django.conf import settings
from exchange import models
from jinja2.filters import do_truncate

from snippets.jinja2 import environment

jinja2_env = environment()


def truncate_passage(passage):
    """
    Обрезка последовательности до 512 (теоретический предел модели),
    дабы сэкономить трафик и память
    """
    return do_truncate(jinja2_env, passage, 512, end='')


def passages_generator(source_site=None):
    qs = models.StackExchangePost.objects.filter(
        source_type=1
    ).exclude(
        most_voted_answer__isnull=True
    )

    if source_site:
        qs = qs.filter(source_site=source_site)

    for post in qs.iterator():
        if not post.body_cleaned and not post.title_cleaned:
            continue

        if post.title_cleaned:
            yield post.id, post.most_voted_answer_id, 3, post.title_cleaned

        if post.body_cleaned:
            passage = truncate_passage(post.body_cleaned)
            yield post.id, post.most_voted_answer_id, 2, passage

        answers = post.children.filter(
            source_type=2,
            body_cleaned__isnull=False,
            score__gt=0
        ).exclude(body_cleaned='').only('id', 'body_cleaned')

        for answer in answers:
            passage = truncate_passage(answer.body_cleaned)
            yield post.id, answer.id, 1, passage


def export_passages(file_path=None, source_site=None):
    if file_path is None:
        file_path = os.path.join(
            settings.PROJECT_DIR, 'export_data', 'passages.csv'
        )

    with open(file_path, 'w') as csvfile:
        writer = csv.writer(
            csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL
        )

        i = 0
        for post_id, answer_id, sentence_type, passage in passages_generator(
            source_site=source_site
        ):
            i += 1

            if i % 1000 == 0:
                passage_print = passage.replace("\n", " ")
                print(
                    f'{(str(i) + ")").ljust(12)}'
                    f'{str(post_id).ljust(12)}'
                    f'{str(answer_id).ljust(12)}'
                    f'{sentence_type}: '
                    f'{passage_print}'
                )

            writer.writerow((post_id, answer_id, sentence_type, passage))
