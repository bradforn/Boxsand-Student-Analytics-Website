# Generated by Django 2.1 on 2018-08-06 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_remove_course_question_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='pub_date',
        ),
    ]
