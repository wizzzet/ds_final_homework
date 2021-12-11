from snippets.enums import StatusEnum


def activate(modeladmin, request, queryset):
    queryset.update(is_active=True)


activate.short_description = 'Активировать'


def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)


deactivate.short_description = 'Деактивировать'


def draft(modeladmin, request, queryset):
    queryset.update(status=StatusEnum.DRAFT)


draft.short_description = 'В черновики'


def hide(modeladmin, request, queryset):
    queryset.update(status=StatusEnum.HIDDEN)


hide.short_description = 'Скрыть'


def publish(modeladmin, request, queryset):
    queryset.update(status=StatusEnum.PUBLIC)


publish.short_description = 'Опубликовать'
