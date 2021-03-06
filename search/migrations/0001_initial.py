# Generated by Django 3.2.5 on 2021-08-25 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=300)),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('rent', models.CharField(max_length=200)),
                ('layout', models.CharField(max_length=200)),
                ('area', models.CharField(max_length=200)),
                ('station', models.CharField(max_length=200)),
                ('timeOnFoot', models.CharField(max_length=200)),
                ('age', models.CharField(max_length=200)),
                ('difference', models.FloatField()),
                ('bargain', models.BooleanField()),
            ],
        ),
    ]
