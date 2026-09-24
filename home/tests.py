from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Category, Order, Product, CustomerProfile


EXPECTED_IMAGE_PATH = "products/71N8YkTS0TL_n18lQBY_SN7HfU1._AC_UF10001000_QL80_.jpg"


class StorefrontTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Phones")
        Product.objects.create(
            category=self.category,
            name="Galaxy S26",
            description="Flagship smartphone",
            price=999.00,
            stock=10,
            featured=True,
        )

    def test_home_page_renders_professional_storefront(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Professional")
        self.assertContains(response, "All Products")
        self.assertContains(response, "theme-toggle")
        self.assertContains(response, "Browse our full collection")

    def test_checkout_page_is_available_for_cart_items(self):
        user = get_user_model().objects.create_user(username="tester", password="secret123")
        self.client.force_login(user)

        session = self.client.session
        session["cart"] = {str(self.category.id): 1}
        session.save()

        response = self.client.get(reverse("checkout"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Checkout")

    def test_new_order_is_placed_and_customer_sees_updated_status(self):
        user = get_user_model().objects.create_user(username="buyer", password="secret123")
        order = Order.objects.create(user=user, total_price="999.00")
        self.assertEqual(order.status, Order.STATUS_PLACED)

        order.status = Order.STATUS_CONFIRMED
        order.save(update_fields=["status"])
        self.client.force_login(user)

        response = self.client.get(reverse("orders"))

        self.assertContains(response, "Confirmed")
        self.assertNotContains(response, "Status: Completed")

    def test_registration_requires_10_digit_phone_number(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "phone_number": "abcd123456",
                "password": "secret123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter exactly 10 digits")

    def test_customer_profile_page_shows_user_details(self):
        user = get_user_model().objects.create_user(
            username="profileuser",
            email="profile@example.com",
            password="secret123",
            first_name="Aisha",
            last_name="Patel",
        )
        profile = CustomerProfile.objects.create(user=user, phone_number="9876543210")
        self.client.force_login(user)

        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Customer Profile")
        self.assertContains(response, "profileuser")
        self.assertContains(response, "profile@example.com")
        self.assertContains(response, "Aisha Patel")
        self.assertContains(response, "9876543210")

    def test_product_image_assignment_is_preserved(self):
        product = Product.objects.get(name="Galaxy S26")
        product.image = EXPECTED_IMAGE_PATH
        product.save()

        product.refresh_from_db()

        self.assertEqual(product.image.name, EXPECTED_IMAGE_PATH)
