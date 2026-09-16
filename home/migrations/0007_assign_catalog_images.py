from django.db import migrations
from django.db.models import Q


IMAGE_BY_CATEGORY = {
    "Phones": "products/samsung26.jpg",
    "Tablets": "products/samsung_tab.jpg",
    "Laptops": "products/Laptop.jpg",
    "TVs": "products/samsungtv.jpg",
}


def assign_images(apps, schema_editor):
    Category = apps.get_model("home", "Category")
    Product = apps.get_model("home", "Product")

    for category_name, image_path in IMAGE_BY_CATEGORY.items():
        category = Category.objects.filter(name=category_name).first()
        if category:
            Product.objects.filter(
                Q(category=category),
                Q(image="") | Q(image__isnull=True),
            ).update(image=image_path)


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0006_samsung_catalog"),
    ]

    operations = [
        migrations.RunPython(assign_images, migrations.RunPython.noop),
    ]