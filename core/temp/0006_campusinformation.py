# Generated by Django 4.0.1 on 2022-06-06 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_programinformation'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampusInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campus_name', models.CharField(max_length=255)),
            ],
        ),
    ]
