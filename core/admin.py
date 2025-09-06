from django.contrib import admin
from core.models import Product,Category,Vendor,CartOrderItems,CartOrder,wishlist,Address,ProductImage,ProductReviews

class ProductImagesAdmin(admin.TabularInline):
    model=ProductImage
    
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display=['pid','user','title','product_image','price','popular','product_status','Category','vendor','get_percentage']
    
    
    
class CategoryAdmin(admin.ModelAdmin):
    list_display=['title','category_image','cid']


class VendorAdmin(admin.ModelAdmin):
    list_display=['title','vendor_image','vid','address','contact','description','date','cover_image']




class CartOrderAdmin(admin.ModelAdmin):
    list_display=['user','price','paid_track','order_date','product_status']
    
    
    
class CartOrderItemAdmin(admin.ModelAdmin):
    list_display=['order','invoice_no','product_status','item','image','qry','price','total']
    
    
class ProductReviewAdmin(admin.ModelAdmin):
    list_display=['user','product','review','rating','date']
    
    
class WishlistAdmin(admin.ModelAdmin):
    list_display=['user','product','date']
      
    
class AddressAdmin(admin.ModelAdmin):
    list_display=['user','address','status']
    
    

admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(CartOrder,CartOrderAdmin)
admin.site.register(CartOrderItems,CartOrderItemAdmin)
admin.site.register(wishlist,WishlistAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(ProductReviews,ProductReviewAdmin)





# Register your models here.