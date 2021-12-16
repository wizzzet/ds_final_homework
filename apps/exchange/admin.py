from django.contrib import admin
from import_export.admin import ExportMixin
from import_export.formats import base_formats

from exchange import models, sync


@admin.register(models.StackExchangePost)
class StackExchangePostAdmin(ExportMixin, admin.ModelAdmin):
    """Записи StackExchange"""

    fields = models.StackExchangePost().collect_fields()
    formats = [base_formats.CSV, base_formats.XLS, base_formats.XLSX]
    list_display = (
        'source_id', 'title_cleaned', 'body_short', 'comments_count',
        'answers_count', 'score', 'source_created', 'last_trained'
    )
    list_filter = ('source_type', 'source_site')
    list_per_page = 50
    raw_id_fields = ('most_voted_answer', 'parent')
    readonly_fields = tuple(fields)
    resource_class = sync.StackExchangePostResource
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
