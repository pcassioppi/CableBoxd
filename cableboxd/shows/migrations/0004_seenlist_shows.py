# Generated by Django 2.1.4 on 2021-02-03 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0003_auto_20210203_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='seenlist',
            name='shows',
            field=models.ManyToManyField(to='shows.Show'),
        ),
    ]