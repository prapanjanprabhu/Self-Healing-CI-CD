from django.db import models

class AdminUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.username



from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class GiftUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email



class LoginLog(models.Model):
    user = models.ForeignKey(GiftUser, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)








class PageContent(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    welcome_message = models.CharField(max_length=255)
    about_company = models.TextField()
    order_button_text = models.CharField(max_length=100)
    order_button_link = models.CharField(max_length=255, default="#")
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    contact_address = models.TextField()
    tagline = models.CharField(max_length=255)
    def __str__(self):
        return "Home Page Content"

from django.utils.text import slugify

class TopSearch(models.Model):
    keyword = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    redirect_url = models.URLField(blank=True, null=True) 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.keyword)
        super().save(*args, **kwargs)













from django.db import models
from decimal import Decimal

class AffiliateProduct(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(null=True,max_length=5000)
    name = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.title



    @property
    def total_price(self):
        return self.price + self.service_fee
    

class Cart(models.Model):
    user = models.ForeignKey(GiftUser, on_delete=models.CASCADE)
    product = models.ForeignKey(AffiliateProduct, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # prevent duplicate cart entries

    def __str__(self):
        return f"{self.user.email} - {self.product.title}"




class AffiliateProductImage(models.Model):
    product = models.ForeignKey(AffiliateProduct, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=5000)

    def __str__(self):
        return f"Image for {self.product.title}"


from django.db import models
from decimal import Decimal



class GiftOrder(models.Model):
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    receiver_name = models.CharField(max_length=100)
    receiver_address = models.TextField()
    landmark = models.CharField(max_length=100,default="",null=True)
    pincode = models.CharField(max_length=100,default="",null=True)
    district = models.CharField(max_length=100,default="",null=True)
    preferences = models.TextField()
    occasion = models.CharField(max_length=100)
    product = models.ForeignKey('AffiliateProduct', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, default='Pending')  # Use 'Pending' or 'Approved'



    def __str__(self):
        return f"{self.sender_name} → {self.receiver_name} ({self.occasion})"
