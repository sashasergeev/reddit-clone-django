# Generated by Django 3.2.6 on 2021-09-09 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_subreddit_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(blank=True, max_length=1200),
        ),
    ]
