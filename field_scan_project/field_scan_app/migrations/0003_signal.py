# Generated by Django 5.0.3 on 2024-03-31 00:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('field_scan_app', '0002_rename_projectblank_imagefile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease', models.PositiveSmallIntegerField()),
                ('health', models.PositiveSmallIntegerField()),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='field_scan_app.imagefile')),
            ],
        ),
    ]
