# Generated by Django 4.1.7 on 2023-04-20 19:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0005_remove_bid_max_bid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bid",
            name="bid",
        ),
        migrations.AddField(
            model_name="bid",
            name="bid",
            field=models.ManyToManyField(
                blank=True, related_name="bids", to="auctions.auctionlisting"
            ),
        ),
    ]
