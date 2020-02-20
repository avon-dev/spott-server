# Generated by Django 3.0.1 on 2020-02-20 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0039_auto_20200220_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='testapp_notice_comment_related', to='testapp.Comment'),
        ),
    ]
