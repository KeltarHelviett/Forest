# Generated by Django 2.0.4 on 2018-05-24 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ForestSN', '0006_userimage_pub_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='publication date')),
                ('text', models.TextField(blank=True, max_length=1000)),
                ('author_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('parent_post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_post_set', to='ForestSN.Post')),
                ('root_post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='root_post_set', to='ForestSN.Post')),
            ],
        ),
    ]
