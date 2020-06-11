# Generated by Django 3.0.5 on 2020-04-07 10:17

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nickname', models.CharField(blank=True, max_length=40, null=True, verbose_name='昵称')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('gender', models.CharField(choices=[('M', '男'), ('F', '女')], default='M', max_length=1, verbose_name='性别')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='居住地')),
                ('description', models.CharField(blank=True, max_length=400, null=True, verbose_name='个人描述')),
                ('image', models.ImageField(blank=True, default='image/default_user.png', null=True, upload_to='image/%Y/%m', verbose_name='用户头像')),
                ('confirmed', models.BooleanField(default=False, verbose_name='用户确认')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='关注时间')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user_set', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user_set', to=settings.AUTH_USER_MODEL, verbose_name='关注')),
            ],
            options={
                'verbose_name': '用户关系',
                'verbose_name_plural': '用户关系',
            },
        ),
        migrations.CreateModel(
            name='CheckCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_code', models.CharField(max_length=8, verbose_name='验证码')),
                ('add_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户验证码',
                'verbose_name_plural': '用户验证码',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='users',
            field=models.ManyToManyField(related_name='user_relation_user', through='user.UserRelationship', to=settings.AUTH_USER_MODEL, verbose_name='关注'),
        ),
    ]
