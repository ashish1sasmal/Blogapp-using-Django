# Generated by Django 3.1.1 on 2021-05-20 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]