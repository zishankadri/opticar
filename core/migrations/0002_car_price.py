# Generated by Django 5.0.6 on 2024-05-27 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='price',
            field=models.FloatField(default=29),
            preserve_default=False,
        ),
    ]
