# Generated by Django 4.0 on 2022-06-18 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podserver', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='raghu_palash', max_length=30),
            preserve_default=False,
        ),
    ]
