from django.db import models
from common.utils import validate_image,generate_unique_slug
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    category_slug=models.SlugField(max_length=100,unique=True,blank=True,editable=False)

    def save(self,*args,**kwargs):
        if not self.category_slug:
            generate_unique_slug(self,slug_field='category_slug')
        super().save(*args,**kwargs)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural="Categories"

class Product(models.Model):
    image=models.ImageField(upload_to='product_images/',blank=True,null=True,validators=[validate_image])
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=9,decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.PROTECT,related_name="product")
    product_slug=models.SlugField(max_length=100,unique=True,blank=True,editable=False)

    def save(self,*args,**kwargs):
        if not self.product_slug:
            generate_unique_slug(self,slug_field='product_slug')
        super().save(*args,**kwargs)
    
    def __str__(self):
        return self.name