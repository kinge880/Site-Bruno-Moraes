# Generated by Django 5.0.1 on 2025-03-24 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='excerpt',
            field=models.CharField(blank=True, help_text='Resumo ou introdução da postagem', max_length=255),
        ),
    ]
