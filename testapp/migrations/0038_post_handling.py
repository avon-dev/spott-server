# Generated by Django 3.0.1 on 2020-02-20 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0037_remove_post_handling'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='handling',
            field=models.IntegerField(choices=[(22000, '검사 전'), (22001, '사진 통과'), (22002, '잘못된 위치정보'), (22003, '부적절한 사진'), (22004, '부적절한 내용')], default=22001, verbose_name='검사'),
        ),
    ]
