from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Category, Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'get_total')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_ordered', 'status', 'is_complete', 'transaction_id', 'get_cart_total')
    list_filter = ('status', 'is_complete', 'date_ordered')
    search_fields = ('id', 'user__username', 'transaction_id')
    list_editable = ('status',)
    inlines = [OrderItemInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'manufactured_date', 'expiry_date', 'image_preview_thumbnail', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('image_preview_large',)

    class Media:
        js = ('admin/js/image_preview.js',)

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {
                'fields': ('category', 'name', 'description', 'price', 'discount_price', 'image_url', 'is_active')
            }),
            ('Product Image', {
                'fields': ('image', 'image_preview_large'),
                'description': 'Upload a product image. Use the preview below to verify the uploaded image.'
            }),
            ('Dates', {
                'fields': ('manufactured_date', 'expiry_date'),
            }),
        )


    def image_preview_thumbnail(self, obj):
        """Small thumbnail shown in the product list — acts as the 'eye' button."""
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank" title="View full image">'
                '<img src="{}" style="height:35px;width:35px;object-fit:cover;border-radius:4px;cursor:pointer;" />'
                '</a>'
                '&nbsp;'
                '<a href="{}" target="_blank" title="View full image" style="'
                'display:inline-flex;align-items:center;justify-content:center;'
                'width:28px;height:28px;border-radius:50%;background:#417690;color:#fff;'
                'text-decoration:none;font-size:16px;vertical-align:middle;" >&#128065;</a>',
                obj.image.url, obj.image.url, obj.image.url
            )
        return mark_safe('<span style="color:#999;">No image</span>')
    image_preview_thumbnail.short_description = 'Image'

    def image_preview_large(self, obj):
        """Large preview shown on the edit page."""
        if obj.image:
            return format_html(
                '<div style="margin:8px 0;">'
                '<img src="{}" style="max-height:250px;max-width:400px;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.15);" />'
                '<br><a href="{}" target="_blank" style="'
                'display:inline-flex;align-items:center;gap:6px;margin-top:8px;padding:6px 14px;'
                'background:#417690;color:#fff;border-radius:4px;text-decoration:none;font-size:13px;">'
                '&#128065; View Full Image</a>'
                '</div>',
                obj.image.url, obj.image.url
            )
        return mark_safe('<span style="color:#999;font-style:italic;">No image uploaded yet. Use the field above to upload one.</span>')
    image_preview_large.short_description = 'Image Preview'
