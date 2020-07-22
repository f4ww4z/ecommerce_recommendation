# Generated by Django 3.0.8 on 2020-07-22 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20200722_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(0, 'Delivering'), (1, 'Completed'), (2, 'Cancelled')], default=0, help_text='<ul><li>0 - Delivering</li><li>1 - Completed</li><li>2 - Cancelled</li></ul>', max_length=1),
        ),
    ]
