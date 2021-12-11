from django.contrib import admin
from exchange import models


@admin.register(models.StackExchangePost)
class StackExchangePostAdmin(admin.ModelAdmin):
    """Записи StackExchange"""

    fields = models.StackExchangePost().collect_fields()
    list_display = (
        'source_id', 'body_short', 'comments_count', 'answers_count', 'score',
        'source_created', 'last_trained'
    )
    list_filter = ('source_type',)
    list_per_page = 50
    readonly_fields = tuple(fields)
    search_fields = ('=id',)  # на большее не хватит без танцев с индексами

    def body_short(self, obj):
        return obj.body_cleaned[:50]

    body_short.short_description = 'Текст, коротко'

    def answers_count(self, obj):
        # без оптимизации, ибо 1:N в такой ситуации во благо
        return obj.children.count()

    answers_count.short_description = 'Кол-во ответов'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
