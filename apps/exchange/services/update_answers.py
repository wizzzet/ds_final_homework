from exchange import models


def update_most_voted_answers():
    qs = models.StackExchangePost.objects.filter(source_type=1)
    print(f'Total: {qs.count()}')

    i = 0
    for obj in qs.iterator():
        i += 1
        if i % 100 == 0:
            print(
                f'{i}) {obj.source_id}: '
                f'{(obj.title_cleaned[:50] or "-").ljust(50)} '
                f'{obj.body_cleaned[:50] or "-"}'
            )

        answer = obj.children.filter(source_type=2).only('id').order_by(
            '-score'
        ).first()
        if answer:
            obj.most_voted_answer_id = answer.id
            obj.save()

    print('Done')
