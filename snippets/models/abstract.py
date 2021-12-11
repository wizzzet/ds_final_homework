from django.db import models
from django.db.models import ForeignKey, Manager, QuerySet

from snippets.models.enumerates import StatusEnum
from snippets.utils.datetime import utcnow

CREATED_VERBOSE = 'Создано'
UPDATED_VERBOSE = 'Обновлено'
LASTMOD_FIELDS = ('created', 'updated')
UTIL_FIELDS = ('id', 'ordering', 'status') + LASTMOD_FIELDS


class IsActiveManager(models.Manager):
    def get_queryset(self):
        return super(IsActiveManager, self).get_queryset().filter(
            is_active=True
        )


class BaseIsActiveModel(models.Model):
    is_active = models.BooleanField('Активен', default=True)

    objects = models.Manager()
    active_objects = IsActiveManager()

    class Meta:
        abstract = True


class DeletableManager(models.Manager):
    def get_queryset(self):
        return super(DeletableManager, self).get_queryset().filter(
            is_deleted=False
        )


class VirtualDeletableMixin(models.Model):
    """Миксин позволяет сделать удаление модели виртуальным"""
    is_deleted = models.BooleanField('Удален', default=False)
    objects = Manager()
    existing_objects = DeletableManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True


class ArchivableManager(models.Manager):
    def get_queryset(self):
        return super(ArchivableManager, self).get_queryset().filter(
            is_archived=False
        )


class ArchivableMixin(models.Model):
    """Миксин для архивации"""
    is_archived = models.BooleanField('Архивировано', default=False)
    objects = Manager()
    existing_objects = ArchivableManager()

    def archive(self, *args, **kwargs):
        self.is_archived = True
        self.save()

    def unarchive(self):
        self.is_archived = False
        self.save()

    class Meta:
        abstract = True


class BaseQuerySet(QuerySet):
    def published(self):
        return self.filter(status__exact=StatusEnum.PUBLIC)

    def hidden(self):
        return self.filter(status__exact=StatusEnum.HIDDEN)

    def draft(self):
        return self.filter(status__exact=StatusEnum.DRAFT)


BaseManager = Manager.from_queryset(BaseQuerySet)
BaseManager.use_for_related_fields = True


class BasicModel(models.Model):
    translation_fields = tuple()
    objects = Manager()

    def collect_fields(self):
        fields = []
        has_status = False
        has_ordering = False
        has_last_mod = False

        for field in self._meta.fields:
            if field.attname == 'status':
                has_status = True

            if field.attname == 'ordering':
                has_ordering = True

            if field.attname in LASTMOD_FIELDS:
                has_last_mod = True

            if field.attname in UTIL_FIELDS:
                continue

            if isinstance(field, ForeignKey):
                fields.append(field.attname.replace('_id', ''))
            else:
                fields.append(field.attname)

        # служебные поля в самый конец
        if has_status:
            fields.append('status')

        if has_ordering:
            fields.append('ordering')

        if has_last_mod:
            fields.extend(LASTMOD_FIELDS)

        return fields

    def __repr__(self):
        return self.__str__()

    class Meta:
        abstract = True


class CreatedModel(models.Model):
    """Base model for all models with created field"""
    created = models.DateTimeField(
        CREATED_VERBOSE, auto_now_add=True, db_index=True
    )

    class Meta:
        abstract = True


class LastModModel(CreatedModel):
    """Base model for all models with created / updated fields"""
    updated = models.DateTimeField(UPDATED_VERBOSE, auto_now=True)

    class Meta:
        abstract = True


class LastModMixin(models.Model):
    """Base model for all models with created / updated fields"""
    created = models.DateTimeField(
        CREATED_VERBOSE, auto_now_add=True, db_index=True
    )
    updated = models.DateTimeField(UPDATED_VERBOSE, auto_now=True)

    class Meta:
        abstract = True


class StatusOrderingModel(models.Model):
    """Base model for all objects"""
    ordering = models.IntegerField('Порядок', default=0, db_index=True)
    status = models.SmallIntegerField(
        'Статус',
        default=StatusEnum.PUBLIC,
        choices=StatusEnum.get_choices()
    )

    class Meta:
        abstract = True


class BaseModel(StatusOrderingModel, BasicModel, LastModModel):
    """
    Base model class for all models having last-mod field
     and status with ordering
    """
    objects = BaseManager()

    class Meta:
        abstract = True


class BaseDictionaryModel(BaseModel):
    title = models.CharField('Заголовок', max_length=255, unique=True)

    translation_fields = ('title',)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title if self.title else str(self.pk)


class ActualQuerySet(BaseQuerySet):
    def actual(self):
        return self.filter(publish_datetime__lte=utcnow())

    def not_actual(self):
        return self.filter(publish_datetime__gt=utcnow())


ActualManager = Manager.from_queryset(ActualQuerySet)
ActualManager.use_for_related_fields = True
