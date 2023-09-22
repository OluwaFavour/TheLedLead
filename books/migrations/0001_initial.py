# Generated by Django 4.2.5 on 2023-09-14 00:34

import books.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image_url', models.ImageField(blank=True, null=True, upload_to=books.models.book_image_path)),
                ('content', models.TextField()),
                ('date_published', models.DateTimeField(auto_now=True)),
                ('published_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'book',
                'verbose_name_plural': 'books',
                'permissions': [('can_publish_book', 'Can publish books')],
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Rating must be at least 1.'), django.core.validators.MaxValueValidator(5, message='Rating must be at most 5.')])),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'rating',
                'verbose_name_plural': 'ratings',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
            },
        ),
    ]