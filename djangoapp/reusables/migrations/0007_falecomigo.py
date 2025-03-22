# Generated by Django 5.0.1 on 2025-03-20 15:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reusables', '0006_propostaprojetolei'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaleComigo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=150)),
                ('telefone', models.CharField(blank=True, max_length=20, null=True)),
                ('descricao', models.TextField(max_length=15000)),
                ('dtmov', models.DateTimeField(default=django.utils.timezone.now)),
                ('visualizado', models.BooleanField(default=False)),
            ],
        ),
    ]
