# Generated by Django 2.2.5 on 2019-12-07 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20191207_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grant',
            name='days',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='grant',
            name='fond',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='grant',
            name='fond_link',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='grant',
            name='label',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='grant',
            name='link',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='grant',
            name='org',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='grant',
            name='rouble',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='grant',
            name='text',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='grant',
            name='time',
            field=models.DateField(null=True),
        ),
    ]
