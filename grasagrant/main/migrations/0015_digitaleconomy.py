# Generated by Django 2.2.7 on 2019-12-23 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20191222_1230'),
    ]

    operations = [
        migrations.CreateModel(
            name='DigitalEconomy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_number', models.CharField(max_length=50, null=True)),
                ('label', models.CharField(max_length=150, null=True)),
                ('date', models.DateField(null=True)),
                ('text', models.TextField()),
                ('link', models.CharField(max_length=300)),
                ('type_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='digital_economy', to='main.Type')),
            ],
        ),
    ]