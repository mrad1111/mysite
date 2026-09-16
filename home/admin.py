from decimal import Decimal

from django import forms
from django.contrib import admin
from django.db import models
from django.db.models import Sum
from django.forms import TextInput
from django.utils.html import format_html
from .models import (
    Category,
    Product,
    Order,
    OrderItem,
    Review,
)


def normalize_price_string(value):
    if value is None:
        return value

    value = str(value).strip().replace(' ', '')
    if not value:
        return ''

    has_comma = ',' in value
    has_dot = '.' in value

    if has_comma and has_dot:
        if value.rfind(',') > value.rfind('.'):
            value = value.replace('.', '').replace(',', '.')
        else:
            value = value.replace(',', '')
    elif has_comma:
        parts = value.split(',')
        if len(parts) > 1 and len(parts[-1]) == 3:
            value = ''.join(parts)
        else:
            value = value.replace(',', '.')

    return value


def format_price_for_display(value):
    if value is None or value == '':
        return ''

    try:
        amount = Decimal(str(value))
    except Exception:
        return str(value)

    return format(amount, ',.2f')


class ProductAdminForm(forms.ModelForm):
    price = forms.CharField(widget=TextInput(attrs={'class': 'vTextField'}))

    class Meta:
        model = Product
        fields = '__all__'

    class Media:
        js = ('home/js/admin_price_format.js',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        price = self.initial.get('price')

        if price is None and self.instance and self.instance.pk:
            price = self.instance.price

        if price is not None:
            self.fields['price'].initial = format_price_for_display(price)

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if isinstance(price, str):
            normalized = normalize_price_string(price)
            if normalized == '':
                return None
            try:
                return Decimal(normalized)
            except Exception:
                raise forms.ValidationError('Enter a valid price.')

        return price


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    formfield_overrides = {
        models.DecimalField: {
            'widget': TextInput(attrs={'class': 'vTextField'})
        },
    }

    list_display = (
        "id",
        "name",
        "category",
        "price",
        "stock",
        "featured",
    )

    list_editable = ("category", "stock")

    list_filter = (
        "category",
        "featured",
    )

    search_fields = (
        "name",
        "description",
    )

    list_per_page = 15
    ordering = ("-id",)

    fieldsets = (
        ("Product Details", {
            "fields": ("name", "category", "description", "image", "price", "stock", "featured")
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total_price",
        "status",
        "created_at",
    )
    list_editable = ("status",)
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            total_sales = Order.objects.aggregate(total=Sum("total_price"))["total"] or 0
            order_count = Order.objects.count()
            latest_order = Order.objects.order_by("-created_at").first()
            response.context_data["summary"] = {
                "total_sales": total_sales,
                "order_count": order_count,
                "latest_order": latest_order,
            }
        except Exception:
            pass
        return response


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product",
        "quantity",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "user",
        "rating",
        "created_at",
    )

    list_filter = (
        "rating",
    )