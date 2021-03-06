# Generated by Django 3.0.5 on 2020-04-25 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('c19map', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='age',
            field=models.IntegerField(default=18),
        ),
        migrations.AddField(
            model_name='person',
            name='cabeza',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='person',
            name='garganta',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='person',
            name='respiracion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='person',
            name='sex',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='person',
            name='tos',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(default='a@example.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='person',
            name='latitude',
            field=models.FloatField(default=23.0),
        ),
        migrations.AlterField(
            model_name='person',
            name='longitude',
            field=models.FloatField(default=-102.0),
        ),
        migrations.AlterField(
            model_name='person',
            name='temperature',
            field=models.FloatField(default=36.5),
        ),
    ]
