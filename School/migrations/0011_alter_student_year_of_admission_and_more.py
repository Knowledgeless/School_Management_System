# Generated by Django 4.1.7 on 2025-01-11 12:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('School', '0010_alter_student_year_of_admission_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='year_of_admission',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='year_of_joining',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]