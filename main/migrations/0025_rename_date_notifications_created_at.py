# Generated by Django 3.2.6 on 2021-10-01 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_notifications'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notifications',
            old_name='date',
            new_name='created_at',
        ),
    ]
