# Generated by Django 4.2 on 2023-04-24 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

from baham.constants import TOWNS


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('baham', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthdate', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('type', models.CharField(choices=[('OWNER', 'OWNER'), ('COMPANION', 'COMPANION')], max_length=10)),
                ('primary_contact', models.CharField(max_length=20)),
                ('alternate_contact', models.CharField(max_length=20, null=True)),
                ('address', models.CharField(max_length=255)),
                ('address_latitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('address_longitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('landmark', models.CharField(max_length=255)),
                ('town', models.CharField(choices=[(c, c) for c in TOWNS], max_length=50)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('date_deactivated', models.DateTimeField(editable=False, null=True)),
                ('bio', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='companion',
            name='user_ptr',
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contract',
            name='companion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baham.userprofile'),
        ),
        migrations.DeleteModel(
            name='Owner',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='Companion',
        ),
    ]
