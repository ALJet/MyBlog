# Generated by Django 3.0.5 on 2020-04-07 10:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='文章标题')),
                ('content', models.TextField(blank=True, null=True, verbose_name='文章内容')),
                ('pub_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('recommend', models.BooleanField(default=False, verbose_name='是否推荐')),
                ('read_nums', models.IntegerField(default=0, verbose_name='浏览量')),
                ('is_anonymous', models.BooleanField(default=False, verbose_name='匿名文章')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'ordering': ['-pub_time'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ip', models.CharField(blank=True, max_length=30, null=True)),
                ('content', models.TextField(blank=True, null=True, verbose_name='评论内容')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='评论时间')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='话题')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='话题描述')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('image', models.ImageField(blank=True, default='image/default_topic.jpg', null=True, upload_to='image/%Y/%m/', verbose_name='话题图片')),
            ],
            options={
                'verbose_name': '话题',
                'verbose_name_plural': '话题',
            },
        ),
        migrations.CreateModel(
            name='UserCollectArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户收藏文章',
                'verbose_name_plural': '用户收藏文章',
            },
        ),
        migrations.CreateModel(
            name='UserFollowArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户关注文章',
                'verbose_name_plural': '用户关注文章',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField(default=1, verbose_name='投票数')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投票时间')),
                ('give_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote', to='blog.Article', verbose_name='投票者')),
            ],
        ),
    ]
