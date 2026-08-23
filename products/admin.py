from django.contrib import admin
from products.models import Product,Category
from django.utils.html import format_html
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name','category_slug']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','image_preview','name','product_slug','description','price','category']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = 'Preview'