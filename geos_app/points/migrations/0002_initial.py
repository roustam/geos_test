# Generated by Django 4.2.6 on 2023-10-11 08:53

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('points', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PointsModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('obj_id', models.IntegerField(default=0)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LinesModel',
            fields=[
                ('line_id', models.AutoField(primary_key=True, serialize=False)),
                ('from_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_point', to='points.pointsmodel')),
                ('to_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_point', to='points.pointsmodel')),
            ],
        ),
    ]