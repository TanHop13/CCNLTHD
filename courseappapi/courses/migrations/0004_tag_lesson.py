# Generated by Django 5.0.3 on 2024-03-07 03:48

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_course_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('updated_to', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('updated_to', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('subject', models.CharField(max_length=255)),
                ('content', ckeditor.fields.RichTextField(null=True)),
                ('image', models.ImageField(upload_to='courses/%Y/%m')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('tag', models.ManyToManyField(to='courses.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
