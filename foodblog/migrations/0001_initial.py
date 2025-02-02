# Generated by Django 4.2 on 2025-01-20 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('genre', models.CharField(max_length=100)),
                ('sub_genre', models.CharField(blank=True, max_length=100, null=True)),
                ('access', models.CharField(max_length=255)),
                ('station', models.CharField(max_length=100)),
                ('mobile_url', models.URLField()),
                ('photo_large', models.URLField(blank=True, null=True)),
                ('photo_medium', models.URLField(blank=True, null=True)),
                ('business_hours', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
