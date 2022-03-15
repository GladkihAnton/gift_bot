# Generated by Django 4.0.2 on 2022-03-15 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_hobby_unique hobby name'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='suggestedgift',
            name='unique suggested gift',
        ),
        migrations.AddConstraint(
            model_name='suggestedgift',
            constraint=models.UniqueConstraint(fields=('customer_id', 'gift_id', 'recipient_id'), name='unique suggested gift'),
        ),
    ]
