# Generated by Django 4.1.7 on 2025-01-09 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('School', '0002_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='full_name',
            field=models.CharField(default='give_me_name', max_length=255),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Teacher', 'Teacher'), ('Student', 'Student')], max_length=10),
        ),
        migrations.AlterField(
            model_name='student',
            name='class_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='student',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='School.profile'),
        ),
        migrations.AlterField(
            model_name='student',
            name='section',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='student',
            name='year_of_admission',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]