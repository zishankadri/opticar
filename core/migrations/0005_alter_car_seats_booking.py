# Generated by Django 5.0.6 on 2024-06-18 10:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_car_seats'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='seats',
            field=models.IntegerField(choices=[(2, '2 seats'), (4, '4 seats'), (6, '6 seats')]),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pick_up_datetime', models.DateTimeField()),
                ('drop_off_datetime', models.DateTimeField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
