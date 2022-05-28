from django.urls import reverse_lazy
from distutils.command.upload import upload
from pickle import TRUE
from tabnanny import verbose
from django.db import models

# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=100,unique=TRUE)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=255,blank=True)
    cat_image=models.ImageField(upload_to='photos/categories',blank=True)


    class Meta:
        verbose_name="category"
        verbose_name_plural='categories'


    def get_url(self):
        #  reverse('',args=[self.slug])
        return reverse_lazy('my_store:products_by_category',args=[self.slug])



    def __str__(self) -> str:
        return self.category_name



