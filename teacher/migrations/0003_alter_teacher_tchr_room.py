# Generated by Django 4.2.6 on 2023-10-27 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_rename_teacher_profile_pic_teacher_tchr_profile_pic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='tchr_room',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
