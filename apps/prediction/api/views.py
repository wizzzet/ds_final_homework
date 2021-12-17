from drf_yasg.utils import swagger_auto_schema
from exchange import models
from rest_framework.response import Response
from rest_framework.views import APIView

from snippets.api.swagger.schema import common_openapi_params
from snippets.api.views import PublicViewMixin

from . import model
from .params import query_param
from .serializers import SearchQuerySerializer


class PredictView(PublicViewMixin, APIView):
    @swagger_auto_schema(
        query_serializer=SearchQuerySerializer(),
        **common_openapi_params(query_param)
    )
    def get(self, request, **kwargs):
        serializer = SearchQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data['query']
        hits = model.predict(query, reranked_results=10)

        answer_ids = [x['answer_id'] for x in hits]
        posts_qs = models.StackExchangePost.objects.filter(
            id__in=answer_ids
        ).select_related('parent')
        answers = {p.id: p for p in posts_qs}

        results = []
        for hit in hits:
            answer = answers.get(int(hit['answer_id']))
            if answer and answer.parent_id:
                results.append({
                    'post': {
                        'id': int(hit['post_id']),
                        'source_id': answer.parent.source_id,
                        'title': answer.parent.title or None,
                        'body': answer.parent.body or None
                    },
                    'answer': {
                        'id': int(hit['answer_id']),
                        'source_id': answer.source_id,
                        'body': answer.body if answer.body else None
                    },
                    'score': hit['score'],
                    'cross_score': hit['cross_score'],
                    'passage': hit['passage']
                })

        return Response(results)
