# Generated by Django 4.2.5 on 2023-11-03 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theblog', '0032_rename_header_image_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateField(auto_now_add=True),
        ),
    ]
