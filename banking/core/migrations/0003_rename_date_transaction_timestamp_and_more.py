# Generated by Django 5.1.3 on 2024-11-18 07:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_transaction_receiver_alter_transaction_sender_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='date',
            new_name='timestamp',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_transactions', to='core.account'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_transactions', to='core.account'),
        ),
    ]
