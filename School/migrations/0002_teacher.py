# Generated by Django 4.1.7 on 2025-01-09 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('School', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='School.profile')),
            ],
        ),
    ]