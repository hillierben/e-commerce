# Generated by Django 4.1.7 on 2023-04-23 07:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0019_alter_watchlist_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="auctionlisting",
            name="user_id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
