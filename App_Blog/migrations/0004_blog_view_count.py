# Generated by Django 5.1.4 on 2025-02-23 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Blog', '0003_alter_blog_options_alter_comment_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
