# Generated by Django 4.0 on 2021-12-16 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0002_alter_stackexchangepost_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stackexchangepost',
            name='source_parent_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Идентификатор родителя в источнике'),
        ),
    ]
