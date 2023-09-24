# Generated by Django 4.2.3 on 2023-09-22 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(blank=True, default=None, null=True)),
                ('user_email', models.EmailField(blank=True, default=None, max_length=254, unique=True)),
                ('account_balance', models.DecimalField(decimal_places=1, default=0, max_digits=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
    ]
