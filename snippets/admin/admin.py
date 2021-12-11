from django.contrib import admin
from django.contrib.admin import ModelAdmin

from snippets.admin import draft, hide, publish
from snippets.utils.array import move_list_element_to_end


class SuperUserDeletableAdminMixin(object):
    @staticmethod
    def has_delete_permission(request, obj=None):
        return request.user.is_superuser


class BaseModelAdmin(ModelAdmin):
    """Базовый класс для админ.части модели BaseModel"""
    actions = ModelAdmin.actions + [publish, draft, hide]
    list_display = ('id', 'status', 'ordering', 'created')
    list_editable = ('status', 'ordering')
    list_filter = ('status',)
    ordering = ('ordering',)
    readonly_fields = ('created', 'updated')
    search_fields = ['=id']

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(BaseModelAdmin, self).get_fieldsets(request, obj=obj)

        for field in ('created', 'updated'):
            if field not in fieldsets[0][1]['fields']:
                fieldsets[0][1]['fields'].append(field)

        return fieldsets


class BaseDictionaryModelAdmin(SuperUserDeletableAdminMixin, BaseModelAdmin):
    """Базовый класс для админ.части модели BaseDictionaryModel"""
    list_display = ('id', 'title', 'status', 'ordering', 'created')
    list_display_links = ('id', 'title')
    readonly_fields = BaseModelAdmin.readonly_fields + ('is_deleted',)
    search_fields = BaseModelAdmin.search_fields + ['title']


class ModelTranlsationFieldsetsMixin(object):
    group_fieldsets = True

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ModelTranlsationFieldsetsMixin, self).get_fieldsets(
            request, obj=obj
        )

        if not hasattr(self, 'tabs_mapping'):
            return fieldsets

        if fieldsets and fieldsets[0][0] != '':
            fieldsets.insert(0, ('', {'fields': []}))

        fieldsets_to_remove = []
        for i, fieldset in enumerate(fieldsets):
            title = fieldset[0]
            if title in self.tabs_mapping:
                if 'classes' not in fieldset[1]:
                    fieldset[1]['classes'] = ()
                fieldset[1]['classes'] += (
                    ('suit-tab', 'suit-tab-%s' % self.tabs_mapping[title])
                )
            elif i != 0:
                for field in reversed(fieldset[1]['fields']):
                    fieldsets[0][1]['fields'].insert(0, field)
                fieldsets_to_remove.append(fieldset)

        if fieldsets_to_remove:
            for fieldset in fieldsets_to_remove:
                fieldsets.remove(fieldset)

        for field in ('status', 'ordering'):
            if field in fieldsets[0][1]['fields']:
                move_list_element_to_end(fieldsets[0][1]['fields'], field)

        return fieldsets


class BasePageAdmin(admin.ModelAdmin):
    list_display = ('title', 'site', 'created')
    list_filter = ('site',)
    readonly_fields = ('created', 'updated')
    suit_form_tabs = (
        ('general', 'Основное'),
        ('seo', 'SEO')
    )


class VirtualDeleteAdminMixin(object):
    readonly_fields = ('is_deleted',)
    list_filter = ('is_deleted',)

    @staticmethod
    def suit_row_attributes(obj, request):
        return {'class': 'is-deleted' if obj.is_deleted else ''}
