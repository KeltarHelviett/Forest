# Generated by Django 2.0.6 on 2018-06-08 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ForestSN', '0015_auto_20180608_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalsocialnetworksession',
            name='access_token',
            field=models.CharField(max_length=256),
        ),
    ]