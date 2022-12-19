# Generated by Django 4.1.3 on 2022-12-19 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0002_alter_image_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="total_likes",
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]
