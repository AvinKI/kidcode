# Generated by Django 5.1.3 on 2024-11-26 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_remove_field_possibility_of_group_registration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='registration_type',
            field=models.CharField(blank=True, choices=[('1', 'انفرادی'), ('2', 'تیمی')], default=1, max_length=20),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile'),
        ),
    ]
