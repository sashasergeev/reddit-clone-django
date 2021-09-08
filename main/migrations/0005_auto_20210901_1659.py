# Generated by Django 3.2.6 on 2021-09-01 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_alter_post_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='subreddit',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sub_admin', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subreddit',
            name='members',
            field=models.ManyToManyField(related_name='sub_members', to=settings.AUTH_USER_MODEL),
        ),
    ]