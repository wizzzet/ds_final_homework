from import_export import resources
from users import models


class UserResource(resources.ModelResource):
    class Meta:
        fields = (
            'id', 'first_name', 'last_name', 'is_active', 'email', 'phone',
            'date_joined', 'is_staff'
        )
        export_order = fields[:]
        model = models.User
        skip_unchanged = True
