# Generated by Django 5.0.6 on 2024-07-26 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_useraccount_verified_details_alter_useraccount_ic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='verified_details',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='verified_email',
            field=models.BooleanField(default=True),
        ),
    ]
