from django.contrib import admin
import admin_thumbnails

# Register your models here.

from .models import Product, ProductGallery,Variation


# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1  #for One choose file field, will show

class variationInline(admin.TabularInline):
    model = Variation
    extra = 1  #for One choose file field, will show

    
    

    
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline,variationInline]




admin.site.register(Product, ProductAdmin)
admin.site.register(Variation,VariationAdmin )
admin.site.register(ProductGallery)

#  02_createsuperuser:
#         command: "echo \"from accounts.models import Account; Account.objects.create_superuser('shah','hussain','admin@gmail.com','admin','khanbbbb')\" | python manage.py shell"
#         leader_only: true