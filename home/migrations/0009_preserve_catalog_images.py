from django.db import migrations


IMAGE_BY_PRODUCT = {
    "Samsung Galaxy S26 Ultra": "products/samsung26.jpg",
    "Samsung Galaxy S26": "products/71N8YkTS0TL_n18lQBY_SN7HfU1._AC_UF10001000_QL80_.jpg",
    "Samsung Galaxy Z Fold8": "products/images_4_nEiGfRo_R1xYLU3.jpg",
    "Samsung Galaxy Z Flip8": "products/images_5_zZHqu6y.jpg",
    "Samsung Galaxy A56 5G": "products/images_6_5FCpQkQ_aBttKDE.jpg",
    "Samsung Galaxy Tab S11 Ultra": "products/images_ryy4xj7.jpg",
    "Samsung Galaxy Tab S10 FE": "products/71hU7ie9N2L_CEs1VRl._AC_UF350350_QL80_.jpg",
    "Samsung Galaxy Tab A9+": "products/images_1_2kXiZPE.jpg",
    "Samsung Galaxy Book5 Pro": "products/-original-imahzc68vhkfdbgc_r1AvBaO.webp",
    "Samsung Galaxy Book5 360": "products/bTxwPhn0em-nykYWTqwb2-Samsung-Laptop-494494325-i-1-1200Wx1200H_u4eqZym.avif",
    "Samsung Galaxy Book4": "products/Laptop.jpg",
    "Samsung Neo QLED 8K Smart TV": "products/samsungtv.jpg",
    "Samsung OLED S95F Smart TV": "products/us-oled-s95f-qn55s95fafxza-545388057_EaPYYbU.webp",
    "Samsung Crystal UHD 4K Smart TV": "products/images_2_YZ9VgUj.jpg",
    "Samsung The Frame 4K Smart TV": "products/ls03f_50-65a_2_tGps64t.jpg",
    "Samsung Galaxy Buds4 Pro": "products/-original-imahhdjmpgjzbbhr_9k5fP01.webp",
    "Samsung Galaxy Watch8": "products/619tP9hJ1sL_sVTopLI._AC_UF10001000_QL80_.jpg",
    "Samsung Galaxy Watch8 Classic": "products/Review-_Samsung_Galaxy_Watch8_and_Watch8_Classic_rF6bhbs.webp",
    "Samsung 45W USB-C Power Adapter": "products/in-feature-supercharge-your-devices-543189086_1aaZH0m.avif",
    "Samsung Galaxy SmartTag2": "products/images_3_LdYwdtG.jpg",
}


def preserve_images(apps, schema_editor):
    Product = apps.get_model("home", "Product")

    for name, image_path in IMAGE_BY_PRODUCT.items():
        Product.objects.filter(name=name).update(image=image_path)


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0008_order_status"),
    ]

    operations = [
        migrations.RunPython(preserve_images, migrations.RunPython.noop),
    ]