# Generated by Django 2.2.13 on 2021-01-12 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0030_credentialapplication_url_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='credentialapplication',
            name='submission_status',
            field=models.PositiveSmallIntegerField(default=10),
        ),
    ]
