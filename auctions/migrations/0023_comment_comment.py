# Generated by Django 4.1.7 on 2023-04-23 19:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0022_comment_listing_comment_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="comment",
            field=models.TextField(default="Add Comment", max_length=200),
        ),
    ]
