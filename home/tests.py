from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Category, Order, Product


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
