# Generated by Django 4.0.2 on 2022-03-09 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('username', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128)),
                ('chat_id', models.IntegerField(blank=True, null=True)),
                ('account_status', models.CharField(blank=True, max_length=32, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'customer',
            },
        ),
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('image', models.ImageField(upload_to='media/img_cache/gifts', verbose_name='img')),
                ('file_id', models.CharField(blank=True, max_length=256, null=True)),
                ('description', models.CharField(max_length=256)),
                ('coolness', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=3, max_digits=10)),
                ('link', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'gift',
            },
        ),
        migrations.CreateModel(
            name='GiftType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'gift_type',
            },
        ),
        migrations.CreateModel(
            name='Hobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'hobby',
            },
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'holiday',
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'order_status',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('image', models.ImageField(upload_to='media/img_cache/packages', verbose_name='package_img')),
                ('file_id', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'db_table': 'package',
            },
        ),
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=256)),
                ('company_name', models.CharField(max_length=256)),
                ('position', models.CharField(max_length=256)),
                ('birthday', models.DateField()),
                ('contact_info', models.CharField(max_length=256)),
                ('delivery_address', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'recipient',
            },
        ),
        migrations.CreateModel(
            name='Sex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'sex',
            },
        ),
        migrations.CreateModel(
            name='SuggestedGift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checked', models.BooleanField()),
                ('presented', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('gift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.gift')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.recipient')),
            ],
            options={
                'db_table': 'suggested_gift',
            },
        ),
        migrations.AddField(
            model_name='recipient',
            name='gifts',
            field=models.ManyToManyField(related_name='recipients', through='customer.SuggestedGift', to='customer.Gift'),
        ),
        migrations.AddField(
            model_name='recipient',
            name='hobbies',
            field=models.ManyToManyField(related_name='recipients', to='customer.Hobby'),
        ),
        migrations.AddField(
            model_name='recipient',
            name='holidays',
            field=models.ManyToManyField(related_name='recipients', to='customer.Holiday'),
        ),
        migrations.AddField(
            model_name='recipient',
            name='sex',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.sex'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivered_at', models.DateField(blank=True, null=True)),
                ('recipient_score', models.IntegerField(blank=True, null=True)),
                ('order_address', models.CharField(blank=True, max_length=128, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('gift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.gift')),
                ('holiday', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.holiday')),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='customer.package')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.recipient')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customer.orderstatus')),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.AddField(
            model_name='gift',
            name='hobbies',
            field=models.ManyToManyField(related_name='gifts', to='customer.Hobby'),
        ),
        migrations.AddField(
            model_name='gift',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.package'),
        ),
        migrations.AddField(
            model_name='gift',
            name='sex',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customer.sex'),
        ),
        migrations.AddField(
            model_name='gift',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customer.gifttype'),
        ),
        migrations.AddField(
            model_name='customer',
            name='recipients',
            field=models.ManyToManyField(blank=True, default=[], related_name='customers', to='customer.Recipient'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=128, null=True)),
                ('voice', models.FileField(null=True, upload_to='media/voice_cache/')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.recipient')),
            ],
            options={
                'db_table': 'comment',
            },
        ),
        migrations.AddConstraint(
            model_name='suggestedgift',
            constraint=models.UniqueConstraint(fields=('gift_id', 'recipient_id'), name='unique suggested gift'),
        ),
        migrations.AddConstraint(
            model_name='order',
            constraint=models.UniqueConstraint(fields=('gift_id', 'recipient_id'), name='unique ordered gift'),
        ),
    ]