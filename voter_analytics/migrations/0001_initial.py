# Generated by Django 5.1.3 on 2024-11-10 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vid', models.IntegerField()),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('street_number', models.IntegerField()),
                ('street_name', models.TextField()),
                ('apartment_number', models.IntegerField()),
                ('zip_code', models.IntegerField()),
                ('dob', models.DateTimeField()),
                ('dor', models.DateTimeField()),
                ('party', models.CharField(max_length=6)),
                ('precinct', models.IntegerField()),
                ('v20state', models.BooleanField()),
                ('v21town', models.BooleanField()),
                ('v21primary', models.BooleanField()),
                ('v22general', models.BooleanField()),
                ('v23town', models.BooleanField()),
                ('voter_score', models.IntegerField()),
            ],
        ),
    ]