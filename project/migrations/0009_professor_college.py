# Generated by Django 5.1.3 on 2024-12-10 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_course_college_course_subschool_student_college'),
    ]

    operations = [
        migrations.AddField(
            model_name='professor',
            name='college',
            field=models.TextField(default='Boston University'),
            preserve_default=False,
        ),
    ]