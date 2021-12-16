from import_export import resources
from exchange import models


class StackExchangePostResource(resources.ModelResource):
    class Meta:
        fields = (
            'source_id', 'title_cleaned', 'body_cleaned', 'most_voted_answer'
        )
        export_order = fields[:]
        model = models.StackExchangePost
        skip_unchanged = True

    @staticmethod
    def dehydrate_most_voted_answer(obj):
        if obj.most_voted_answer_id:
            return (
                obj.most_voted_answer.title_cleaned
                + ' '
                + obj.most_voted_answer.body_cleaned
            ).strip()
        return ''
