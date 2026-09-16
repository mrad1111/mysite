from django.db import migrations


CATALOG = {
    "Phones": [
        ("Samsung Galaxy S26 Ultra", "Flagship Galaxy smartphone with an advanced camera system, vivid display, and all-day performance.", "149999.00"),
        ("Samsung Galaxy S26", "Premium Galaxy smartphone with a bright display, fast performance, and a versatile camera setup.", "79999.00"),
        ("Samsung Galaxy Z Fold8", "Foldable Galaxy phone designed for a larger multitasking workspace and an immersive mobile experience.", "164999.00"),
        ("Samsung Galaxy Z Flip8", "Compact foldable Galaxy phone with a flexible display and a pocket-friendly design.", "109999.00"),
        ("Samsung Galaxy A56 5G", "Reliable 5G smartphone with a smooth display, capable cameras, and long-lasting battery life.", "41999.00"),
    ],
    "Tablets": [
        ("Samsung Galaxy Tab S11 Ultra", "Large-format Galaxy tablet for creative work, entertainment, and focused productivity.", "108999.00"),
        ("Samsung Galaxy Tab S10 FE", "Versatile tablet with a crisp display, S Pen support, and a lightweight everyday design.", "52999.00"),
        ("Samsung Galaxy Tab A9+", "Family-friendly tablet for streaming, browsing, study, and everyday apps.", "19999.00"),
    ],
    "Laptops": [
        ("Samsung Galaxy Book5 Pro", "Premium Windows laptop with a slim metal design, high-resolution display, and efficient performance.", "139990.00"),
        ("Samsung Galaxy Book5 360", "Flexible 2-in-1 laptop with a touch display for work, study, and creative tasks.", "119990.00"),
        ("Samsung Galaxy Book4", "Slim everyday laptop for office work, learning, browsing, and entertainment.", "69990.00"),
    ],
    "TVs": [
        ("Samsung Neo QLED 8K Smart TV", "High-resolution smart TV with vivid contrast, intelligent upscaling, and a cinematic viewing experience.", "249990.00"),
        ("Samsung OLED S95F Smart TV", "Premium OLED television with deep contrast, rich color, and a refined slim profile.", "179990.00"),
        ("Samsung Crystal UHD 4K Smart TV", "Bright 4K smart TV with connected entertainment and an elegant bezel-light design.", "47990.00"),
        ("Samsung The Frame 4K Smart TV", "Art-inspired 4K television that blends entertainment with a refined home display.", "119990.00"),
    ],
    "Accessories": [
        ("Samsung Galaxy Buds4 Pro", "Premium wireless earbuds with immersive sound, active noise control, and a comfortable fit.", "22999.00"),
        ("Samsung Galaxy Watch8", "Connected Galaxy smartwatch for daily wellness, notifications, and activity tracking.", "34999.00"),
        ("Samsung Galaxy Watch8 Classic", "Classic-style smartwatch with health features, fitness tools, and a durable watch design.", "44999.00"),
        ("Samsung 45W USB-C Power Adapter", "Fast USB-C charging adapter for compatible Galaxy phones, tablets, and accessories.", "3499.00"),
        ("Samsung Galaxy SmartTag2", "Compact item tracker that helps you locate everyday essentials from your Galaxy device.", "2999.00"),
    ],
}


def add_catalog(apps, schema_editor):
    Category = apps.get_model("home", "Category")
    Product = apps.get_model("home", "Product")

    for category_name, products in CATALOG.items():
        category, _ = Category.objects.get_or_create(name=category_name)
        for name, description, price in products:
            product, _ = Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "description": description,
                    "price": price,
                    "stock": 10,
                },
            )
            product.category = category
            product.description = description
            product.price = price
            if product.stock == 0:
                product.stock = 10
            product.save(update_fields=["category", "description", "price", "stock"])


def remove_catalog(apps, schema_editor):
    Product = apps.get_model("home", "Product")
    Product.objects.filter(name__in=[product[0] for products in CATALOG.values() for product in products]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0005_wishlist"),
    ]

    operations = [
        migrations.RunPython(add_catalog, remove_catalog),
    ]