# Generated by Django 5.1.6 on 2025-02-15 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertype',
            name='phone_no',
            field=models.IntegerField(null=True),
        ),
    ]
