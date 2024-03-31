# Generated by Django 4.1.4 on 2023-05-19 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0002_remove_userprofile_faculty_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="role",
            name="name",
            field=models.CharField(
                choices=[
                    ("Админ", "Админ"),
                    ("Председател", "Председател"),
                    ("Протоколчик", "Протоколчик"),
                    ("Член на УС", "Член на УС"),
                    ("Член на клуба", "Член на клуба"),
                    ("Студентски съвет", "Студентски съвет"),
                ],
                max_length=255,
            ),
        ),
    ]