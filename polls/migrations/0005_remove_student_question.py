# Generated by Django 2.1 on 2018-08-06 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_remove_course_pub_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='question',
        ),
    ]