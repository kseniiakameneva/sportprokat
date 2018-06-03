from django.db import models
from django.utils import timezone
from django.contrib.admin import widgets
from django.db.models.signals import pre_save
from django.utils.text import slugify
from transliterate import translit
from django.core.urlresolvers import reverse


# from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=100)

    # slug = models.SlugField(blank=True)

    def __str__(self):
        return self.title


'''''''''
    def get_absolute_url(self):
        return reverse('category_detail', (), kwargs={'category.slug': self.slug})


def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(str(instance.title), reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Category)
'''''


class Type(models.Model):
    type = models.CharField(max_length=200)

    # category = models.ForeignKey(Category)

    def __str__(self):
        return self.type


def image_folder(instance, filename):
    filename = instance.title + '.' + filename.split('.')[1]
    return "{0}/{1}".format(instance.title, filename)


'''''''''
class ProductManager(models.Model):
    def all(self, *args, **kwargs):
        return super(ProductManager, self).get_queryset().filter(available=True)
'''''


class Product(models.Model):
    category = models.ForeignKey(Category)
    type = models.ForeignKey(Type, null=True)
    title = models.CharField(max_length=120)
    # slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to=image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


'''''''''
    def get_absolute_url(self):
        return reverse('product_detail', (), kwargs={'product.slug': self.slug})
        

        
class BookedItem(models.Model):
    product = models.ForeignKey(Product)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    
    def __str__(self):
        return "BookedItem {0}".format(self.product.title)
        
        
    class Cart(models.Model):
    items = models.ManyToManyField(BookedItem)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    
    def __str__(self):
        return str(self.id)

'''''
ORDER_STATUS_CHOICES = (
    ('Принято в обработку', 'Принято в обработку'),
    ('Забронировано', 'Забронировано'),
    ('У клиента', 'У клиента'),
    ('Бронь отменена', 'Бронь отменена'),
    ('Заказ выполнен', 'Заказ выполнен')
)


class Order(models.Model):
    product = models.ForeignKey(Product, verbose_name="Название снаряжения")
    name = models.CharField("Ваше имя", max_length=100)
    phone = models.IntegerField("Телефон")
    comment = models.CharField("Ваш комментарий:", max_length=200, blank=True)
    date = models.DateField("Дата начала поездки", default=timezone.now())
    date_end = models.DateField("Дата конца поездки", default=timezone.now())
    stat=models.CharField("Статус",max_length=100, choices= ORDER_STATUS_CHOICES, blank=True)
    def __str__(self):
        return "Бронирование №{0}".format(str(self.id))



class CheckDate(models.Model):
    date = models.DateField("Дата начала поездки", default=timezone.now())
    date_end = models.DateField("Дата конца поездки", default=timezone.now())