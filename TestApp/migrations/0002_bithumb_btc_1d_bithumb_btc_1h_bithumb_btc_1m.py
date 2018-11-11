# Generated by Django 2.1.2 on 2018-11-11 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bithumb_BTC_1d',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('open', models.FloatField()),
                ('close', models.FloatField()),
                ('volume', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Bithumb_BTC_1h',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('open', models.FloatField()),
                ('close', models.FloatField()),
                ('volume', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Bithumb_BTC_1m',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('open', models.FloatField()),
                ('close', models.FloatField()),
                ('volume', models.FloatField()),
            ],
        ),
    ]
