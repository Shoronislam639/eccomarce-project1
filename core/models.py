from django.db import models
from shortuuidfield import ShortUUIDField
from django.utils.html import mark_safe
from userauth.models import User    
from email.policy import default
from pyexpat import model
from unicodedata import decimal





   
STATUS_CHOICE = (
    ('process','Processing'),
    ('shipped','Shipped'),
    ('delivered','Delivered') 
)



STATUS = (
    ('draft','Draft'),
    ('disable','Disable'),
    ('delivered','Delivered'),
    ('rejected','Rejected'),
    ('in_review','In Review'),
    ('published','Published'),
)

RATING = (
    (1,'⭐ ☆☆☆☆'),
    (2,'⭐ ⭐ ☆☆☆'),
    (3,'⭐ ⭐ ⭐ ☆☆'),
    (4,'⭐ ⭐ ⭐ ⭐ ☆'),
    (5,'⭐ ⭐ ⭐ ⭐ ⭐'),
)




def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, max_length=20)  # removed length, prefix, alphabet
    title = models.CharField(max_length=200, default='food')
    image = models.ImageField(upload_to='category',default='category.jpg')
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def category_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        
    def __str__(self):
        return self.title
    
    
class Tags (models.Model):
    pass    
    
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, max_length=20)  # removed length, prefix, alphabet
    
    title = models.CharField(max_length=100, default='Nestify')
    image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
    cover_image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
    description = models.TextField(null=True,blank=True, default='I am amezing vendor')

    
    address = models.CharField(max_length=300, default="123 Street, City, Country")
    contact = models.CharField(max_length=300, default="+8800 123 4567")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shiping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    
    class Meta:
        verbose_name_plural = 'vendors'
        
    def vendor_image(self):
        return mark_safe(f'<img src="%s" width="50" height="50" />'%(self.image.url))
        
    def __str__(self):
        return self.title


class Product(models.Model):
    pid= ShortUUIDField(unique=True, max_length=20)
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,related_name='cetegories')
    vendor = models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True,related_name='vendors')
        
    title = models.CharField(max_length=100, default='Fresh pear')
    image = models.ImageField(upload_to=user_directory_path, default='product.jpg')
    description = models.TextField(null=True,blank=True, default='This is the product')
    
    price = models.DecimalField(max_digits=10, decimal_places=2,default=1.99)
    old_price=models.DecimalField(max_digits=10, decimal_places=2,default=2.59)
    
    specification = models.TextField(null=True,blank=True)
    #tags = models.ForeignKey(Tags,on_delete=models.SET_NULL,null=True)
    
    product_status= models.CharField(choices=STATUS, max_length=10, default='in_review')
    
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    popular = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)


    sku= ShortUUIDField(unique=True, max_length=20,)
    date = models.DateField(auto_now_add=True)
    updated = models.DateField(null=True)
    
    
    class Meta:
        verbose_name_plural = 'Products'
        
    def product_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        
    def __str__(self):
        return self.title
    
    
    def get_percentage(self):
        new_price = (self.old_price - self.price) / self.old_price * 100
        return new_price
    
    
    
class ProductImage (models.Model):
    images = models.ImageField(upload_to='product-images',default='product.jpg')
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    date = models.DateField(auto_now_add=True)
    
    
    class Meta:
        verbose_name_plural = 'Product Images'
        
        
        #############################order##################
        
class CartOrder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    price= models.DecimalField(max_digits=10, decimal_places=2,default=1.99) 
    paid_track=models.BooleanField(default=False)
    order_date= models.DateField(auto_now_add=True)
    product_status=models.CharField(choices=STATUS_CHOICE,max_length=30,default='processing') 


    class Meta:
        verbose_name_plural = 'Cart Order'
        

class CartOrderItems(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=200)
    product_status=models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image=models.CharField(max_length=200)
    qry = models.IntegerField(default=0)
    price= models.DecimalField(max_digits=10, decimal_places=2,default=1.99) 
    total= models.DecimalField(max_digits=10, decimal_places=2,default=1.99) 
    
    
    class Meta:
        verbose_name_plural = 'Cart Order Items'
        
    def order_img(self):
        return mark_safe(f'<img src="/media/%s" width="50" height="50" />'%(self.image))
    
    
    
    
    
    #######################################product review
    
    
class ProductReviews(models.Model):
    user= models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product= models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    review = models.TextField()
    rating=models.IntegerField(default=None,choices=RATING)
    date=models.DateTimeField(auto_now_add=True)
        
    class Meta :
        verbose_name_plural = 'Product Reviews'
            
            
    def __str__(self):
        return self.product.title
        
        
    def get_ratting(self):
        return self.rating
            
        
    

        ########################################  Wishlist   ###########
          
class wishlist(models.Model):
    user= models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product= models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    date=models.DateTimeField(auto_now_add=True)
        
    class Meta :
        verbose_name_plural = 'wishlist'
            
            
    def __str__(self):
         return self.product.title
        
    
class Address(models.Model):
    user= models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=100,null=True)
    status = models.BooleanField(default=False) 
        
        
    class Meta :
        verbose_name_plural = 'Address'