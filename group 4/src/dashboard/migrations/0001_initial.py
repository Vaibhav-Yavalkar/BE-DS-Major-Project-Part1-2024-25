# Generated by Django 5.1.1 on 2024-10-13 19:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.TextField()),
                ('place', models.URLField()),
                ('priority', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='alert_images')),
                ('video', models.FileField(upload_to='alert_vidoes')),
                ('alert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='dashboard.alert')),
            ],
        ),
        migrations.CreateModel(
            name='Updates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('alert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='dashboard.alert')),
            ],
        ),
    ]
