# Generated by Django 3.2.6 on 2021-08-31 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subreddit',
            name='name',
            field=models.CharField(default='post', max_length=150),
        ),
        migrations.AlterField(
            model_name='subreddit',
            name='description',
            field=models.CharField(max_length=250),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('commented_at', models.DateTimeField(auto_now_add=True)),
                ('commentator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.post')),
            ],
        ),
    ]
