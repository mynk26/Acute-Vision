# Generated by Django 3.1.2 on 2020-11-30 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('Subject_Code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('Subject_Name', models.CharField(max_length=50)),
            ],
        ),
    ]
