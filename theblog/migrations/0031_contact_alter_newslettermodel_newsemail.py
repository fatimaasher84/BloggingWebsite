# Generated by Django 4.2.5 on 2023-10-25 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theblog', '0030_alter_post_recipe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('mesg', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='newslettermodel',
            name='newsEmail',
            field=models.EmailField(max_length=100),
        ),
    ]
