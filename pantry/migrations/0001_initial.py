# Generated by Django 3.1 on 2024-09-04 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutCafe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cafe_name', models.CharField(blank=True, max_length=200)),
                ('about', models.TextField(blank=True, max_length=900, null=True)),
                ('cafe_time', models.CharField(blank=True, max_length=200)),
                ('cafe_short_address', models.TextField(blank=True, max_length=500, null=True)),
                ('cafe_full_address', models.TextField(blank=True, max_length=1500, null=True)),
                ('phone_no', models.BigIntegerField(blank=True)),
                ('country', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderd', models.BooleanField(blank=True)),
                ('total_price', models.FloatField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('number_of_People', models.IntegerField(blank=True)),
                ('date_of_booking', models.DateTimeField(blank=True)),
                ('message', models.TextField(blank=True, max_length=500, null=True)),
                ('phone_no', models.BigIntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(blank=True, max_length=300, null=True)),
                ('dish_name', models.CharField(blank=True, max_length=300, null=True)),
                ('dish_discription', models.TextField(blank=True, max_length=500, null=True)),
                ('dish_price', models.IntegerField(blank=True, default=0)),
                ('dish_photo', models.ImageField(help_text='Image size:370 X 370.', upload_to='thumbnail/')),
                ('approval_flag', models.BooleanField(blank=True, default=False)),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pantry.aboutcafe')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pantry.category')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('isOrder', models.CharField(blank=True, max_length=300, null=True)),
                ('total_items', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pantry.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pantry.menu')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
