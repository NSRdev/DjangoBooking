# Generated by Django 3.2.9 on 2021-11-10 23:36

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('size', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('guests', models.IntegerField()),
                ('date_from', models.DateField()),
                ('date_until', models.DateField()),
                ('contact_name', models.CharField(max_length=40)),
                ('contact_email', models.EmailField(max_length=40)),
                ('contact_phone', models.CharField(max_length=9)),
                ('created', models.DateField(auto_now_add=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookingapp.room')),
            ],
        ),
    ]
