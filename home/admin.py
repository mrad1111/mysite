from decimal import Decimal

from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
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
    CustomerProfile,
    Wishlist,
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


class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = "Customer Profile & Contact Info"
    fk_name = "user"


try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    inlines = (CustomerProfileInline,)
    list_display = (
        "id",
        "username",
        "email",
        "get_phone_number",
        "get_order_count",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
        "last_login",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")
    search_fields = ("username", "email", "profile__phone_number")
    ordering = ("-id",)

    def get_phone_number(self, obj):
        if hasattr(obj, "profile") and obj.profile and obj.profile.phone_number:
            return obj.profile.phone_number
        return "-"
    get_phone_number.short_description = "Mobile / Phone"

    def get_order_count(self, obj):
        count = obj.order_set.count()
        if count > 0:
            return format_html('<span class="badge badge-info">{} Orders</span>', count)
        return format_html('<span class="badge badge-secondary">{} Orders</span>', count)
    get_order_count.short_description = "Total Orders"


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "get_email",
        "phone_number",
        "get_date_joined",
        "get_order_count",
    )
    search_fields = ("user__username", "user__email", "phone_number")
    list_filter = ("user__is_active", "user__date_joined")

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email Address"

    def get_date_joined(self, obj):
        return obj.user.date_joined.strftime("%Y-%m-%d %H:%M") if obj.user.date_joined else "-"
    get_date_joined.short_description = "Date Joined"

    def get_order_count(self, obj):
        count = obj.user.order_set.count()
        return f"{count} order(s)"
    get_order_count.short_description = "Orders"


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "product__name")