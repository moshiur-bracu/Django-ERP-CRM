# Generated by Django 3.0.2 on 2020-01-12 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('contact_person', models.TextField()),
                ('address', models.TextField()),
                ('phone_number', models.IntegerField()),
                ('entry_date', models.DateTimeField(auto_now_add=True)),
                ('customer_id', models.CharField(max_length=11)),
                ('customer_status', models.TextField()),
            ],
        ),
    ]