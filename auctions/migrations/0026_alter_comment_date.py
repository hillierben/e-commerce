# Generated by Django 4.1.7 on 2023-04-25 05:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0025_alter_comment_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
