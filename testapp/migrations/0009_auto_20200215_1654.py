# Generated by Django 3.0.1 on 2020-02-15 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0008_auto_20200215_1645'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hashtag',
            old_name='tag_name',
            new_name='name',
        ),
    ]
