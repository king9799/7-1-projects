# Generated by Django 3.2 on 2021-04-21 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forever', '0003_alter_todo_cr_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='cr_on',
            field=models.DateField(auto_now_add=True),
        ),
    ]
