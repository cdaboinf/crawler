# Generated by Django 3.0.8 on 2020-10-22 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surfbrakes', '0004_auto_20201021_1818'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurfWind',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=4)),
                ('date', models.DateTimeField()),
                ('day', models.DateField(blank=True, null=True)),
                ('surfbrake', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='surfbrakes.Surfbrake')),
            ],
        ),
    ]
