# Generated by Django 3.2 on 2021-08-25 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DaySlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spot', models.DateField()),
                ('apartment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='apartment_day_slots', to='listings.listing')),
                ('room', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_day_slots', to='listings.hotelroomtype')),
            ],
        ),
        migrations.AddConstraint(
            model_name='dayslot',
            constraint=models.UniqueConstraint(fields=('spot', 'apartment'), name='apartment_slots'),
        ),
        migrations.AddConstraint(
            model_name='dayslot',
            constraint=models.UniqueConstraint(fields=('spot', 'room'), name='room_slots'),
        ),
    ]
