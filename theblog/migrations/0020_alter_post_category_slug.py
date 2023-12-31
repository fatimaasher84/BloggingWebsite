# Generated by Django 4.2.5 on 2023-10-09 15:10

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theblog', '0019_alter_category_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category_slug',
            field=autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='category'),
        ),
    ]
