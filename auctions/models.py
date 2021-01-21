from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass

class Listing(models.Model):

    class Category(models.TextChoices):
        FASHION = 'FA', _('Fashion')
        TOYS = 'TO', _('Toys')
        ELECTRONICS = 'EL', _('Electronics')
        HOME = 'HO', _('Home')
        OTHERS = 'OT', _('Others')

    title = models.CharField(max_length=64)
    description = models.TextField()
    current_price = models.IntegerField()
    image = models.ImageField(upload_to='listingImages', blank=True)
    category = models.CharField(max_length=64, blank=True, choices=Category.choices)

class Bid(models.Model):
    price = models.IntegerField()

class Comment(models.Model):
    content = models.TextField()