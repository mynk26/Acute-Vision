# Generated by Django 3.1.2 on 2020-12-03 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20201201_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='Department',
            field=models.CharField(choices=[('CSE', 'CSE'), ('IT', 'IT')], max_length=10),
        ),
    ]
