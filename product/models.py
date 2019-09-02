from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.


class Product(models.Model):

    CONDITION_TYPE = (
        ('new', 'NEW'),
        ('fairly used', 'FAIRLY USED')
    )

    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='main_product/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField(null=True)
    email = models.EmailField(max_length=100)
    condition = models.CharField(max_length=100, choices=CONDITION_TYPE)
    price = models.FloatField()
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True)
    views_count = models.IntegerField(default=0)

    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
            super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']

    # class Meta:
        #verbose_name = 'product'
        #verbose_name_plural = 'products'


class Images(models.Model):
    post = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.post.title + " image"

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class Category(models.Model):
    # for product category
    category_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category/', blank=True, null=True)

    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.category_name:
            self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Brand(models.Model):
    # for brand
    brand_name = models.CharField(max_length=50)

    def __str__(self):
        return self.brand_name

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'


class City(models.Model):
    # for city name
    city_name = models.CharField(max_length=50)

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return "Profile of user {}".format(self.user.username)
