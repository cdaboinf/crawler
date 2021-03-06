# Generated by Django 3.0.8 on 2020-09-30 01:14

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Surfbrake',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=100)),
                ('description', models.EmailField(max_length=254)),
                ('tide', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(blank=True, decimal_places=4, max_digits=10), size=None), size=None)),
                ('wind', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(blank=True, decimal_places=4, max_digits=10), size=None), size=None)),
                ('wave_height', models.TextField()),
                ('temperature', models.TextField()),
                ('water_temperature', models.TextField()),
                ('rain_posibility', models.TextField()),
                ('summary', models.TextField()),
                ('active', models.BooleanField()),
                ('station', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='stations.Station')),
            ],
        ),
    ]
