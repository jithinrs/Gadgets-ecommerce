from django.urls import reverse
from django.db import models
from Category.models import Categories,SubCategories
# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(max_length=255)
    brand = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    product_image_1 = models.ImageField(upload_to = 'photos/product',blank = False)
    product_image_2 = models.ImageField(upload_to = 'photos/product', blank = False)
    product_image_3 = models.ImageField(upload_to = 'photos/product', blank = False)
    product_image_4 = models.ImageField(upload_to = 'photos/product',blank = False)
    product_description = models.TextField()
    category_id = models.ForeignKey(Categories,on_delete=models.CASCADE)
    subcategory_id = models.ForeignKey(SubCategories, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
 
    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_detail',args = [self.category_id.slug , self.subcategory_id.slug, self.slug ])