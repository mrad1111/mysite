from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0007_assign_catalog_images"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("placed", "Order placed"),
                    ("confirmed", "Confirmed"),
                    ("completed", "Completed"),
                ],
                default="placed",
                max_length=20,
            ),
        ),
    ]