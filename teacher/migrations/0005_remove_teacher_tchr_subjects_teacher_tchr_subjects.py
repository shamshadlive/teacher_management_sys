# Generated by Django 4.2.6 on 2023-10-27 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_alter_teacher_tchr_room'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='tchr_subjects',
        ),
        migrations.AddField(
            model_name='teacher',
            name='tchr_subjects',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]