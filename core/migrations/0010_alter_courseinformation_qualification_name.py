# Generated by Django 4.0.1 on 2022-11-19 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_courseinformation_course_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseinformation',
            name='qualification_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]