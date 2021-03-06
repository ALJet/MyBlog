# Generated by Django 3.0.5 on 2020-05-07 09:48

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20200415_1056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='topics',
        ),
        migrations.AddField(
            model_name='article',
            name='topics',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(blog.models.get_sentinel_user), related_name='article_topics', to='blog.Topic', verbose_name='话题'),
        ),
    ]
