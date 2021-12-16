from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from import_export.admin import ExportMixin
from import_export.formats import base_formats
from users import sync, models
from users.forms import UserAdminForm, UserCreationForm

from snippets.admin import activate, deactivate

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(DjangoGroupAdmin):
    pass


@admin.register(models.User)
class UserAdmin(ExportMixin, DjangoUserAdmin):
    """Пользователь"""
    actions = DjangoUserAdmin.actions + [activate, deactivate]
    add_form = UserCreationForm
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-basic'),
            'fields': (
                'is_active', 'username', 'password', 'created', 'updated'
            )
        }),
        ('Персональные данные', {
            'classes': ('suit-tab', 'suit-tab-basic'),
            'fields': (
                'last_name', 'first_name', 'email', 'phone', 'birth_date'
            )
        }),
        ('Важные даты', {
            'classes': ('suit-tab', 'suit-tab-basic'),
            'fields': ('last_login', 'date_joined')
        }),
        ('Права доступа', {
            'classes': ('suit-tab', 'suit-tab-permission'),
            'fields': (
                'is_staff', 'is_superuser', 'user_permissions'
            )
        })
    )
    form = UserAdminForm
    formats = [base_formats.CSV, base_formats.XLS, base_formats.XLSX]
    list_display = (
        'username', 'first_name', 'last_name', 'phone', 'email', 'is_active'
    )
    list_display_links = ('username',)
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')
    readonly_fields = ('last_login', 'date_joined', 'created', 'updated')
    resource_class = sync.UserResource
    search_fields = (
        '=id', 'email', 'first_name', 'last_name', 'phone', 'username'
    )
    suit_form_tabs = (
        ('basic', 'Основное'),
        ('permission', 'Права доступа')
    )

    def get_actions(self, request):
        actions = super(UserAdmin, self).get_actions(request)
        if 'delete_selected' in actions and not request.user.is_superuser:
            del actions['delete_selected']
        return actions
