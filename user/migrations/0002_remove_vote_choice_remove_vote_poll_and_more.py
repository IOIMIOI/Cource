# Generated by Django 4.2 on 2023-06-02 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='choice',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='poll',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='testing_id',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='user',
        ),
        migrations.DeleteModel(
            name='TaskAnswer',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
