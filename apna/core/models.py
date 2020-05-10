import uuid
import os
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from PIL import Image
from . import utils


def profile_image_file_path(instance, filename):
    """ Generate file path for new recipe image """
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('pics_profile/', filename)


def product_image_file_path(instance, filename):
    """ Generate file path for new recipe image """
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('pics_product/', filename)


def shop_category_image_file_path(instance, filename):
    """ Generate file path for new recipe image """
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('pics_shop_category/', filename)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """ Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_type_user(self, email, password, user_type):
        """ Creates and saves new type user """
        user = self.create_user(email, password)
        user.user_type = user_type
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """ Creates and saves new super user """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_agent = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('shop', 'shop'),
        ('customer', 'customer'),
        ('delivery', 'delivery'),
        ('owner', 'owner'),
    ]

    username = None
    email = models.EmailField(max_length=255, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='owner')
    is_staff = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, null=True, blank=True, default='')

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class InsertUpdate(models.Model):
    Inserted_By = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inserted_byy', null=True, blank=True)
    Inserted_On = models.DateTimeField(default=timezone.now)
    Updated_By = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='updated_byy')
    Updated_On = models.DateTimeField(null=True, blank=True)


class SetupTable(InsertUpdate, models.Model):
    Name = models.CharField(max_length=255, blank=False)
    Description = models.TextField(max_length=500)
    Is_Active = models.BooleanField(default=True)
    System_Used = models.BooleanField(default=False)

    def __str__(self):
        return self.Name


class Gender(SetupTable):
    pass


class Country(SetupTable):
    class Meta:
        verbose_name_plural = 'Countries'


class City(SetupTable):
    countryy = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='city')

    class Meta:
        verbose_name_plural = 'Cities'


class ProfileStatus(SetupTable):
    class Meta:
        verbose_name_plural = 'Profile Statuses'


class AddressType(SetupTable):
    pass


class ShopCategory(SetupTable):
    image = models.ImageField(default='pics_default/default_shop_category.png', upload_to=shop_category_image_file_path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class ProductCategory(SetupTable):
    Shop_Category = models.ForeignKey(ShopCategory, on_delete=models.CASCADE, related_name='Shop_Categoryy')
    image = models.ImageField(default='pics_default/default_product.jpg', upload_to=product_image_file_path)
    slug = models.SlugField(max_length=255, null=True, blank=True, default='')

    class Meta:
        verbose_name_plural = 'Product Categories'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class ProductSubcategory(SetupTable):
    Product_Category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='ProductCategory')

    class Meta:
        verbose_name_plural = 'Product Subcategories'


class ProductBrand(SetupTable):
    Product_Category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='BrandProductCategory')
    pass


class ProductUnitType(SetupTable):
    pass


class ShopStatus(SetupTable):
    class Meta:
        verbose_name_plural = 'Shop Statuses'


class OrderStatus(SetupTable):
    class Meta:
        verbose_name_plural = 'Order Statuses'


class PaymentStatus(SetupTable):
    class Meta:
        verbose_name_plural = 'Payment Statuses'


class PaymentType(SetupTable):
    pass


class Profile(InsertUpdate, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.DO_NOTHING, related_name='profile_gender', null=True, blank=True)
    Full_Name = models.CharField(max_length=50)
    CNIC = models.BigIntegerField(null=True, blank=True)
    DOB = models.DateField(null=True, blank=True)
    contact = models.BigIntegerField(null=True, blank=True)
    other_contacts = models.TextField(max_length=1000, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True, blank=True)
    WhatsApp = models.BooleanField(default=False)
    Profile_Status = models.ForeignKey(ProfileStatus, on_delete=models.DO_NOTHING, null=True, blank=True)
    image = models.ImageField(default='pics_default/default_user.png', upload_to=profile_image_file_path)

    def __str__(self):
        return f'{self.user.email} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Address(InsertUpdate, models.Model):
    Profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='profile_address')
    Address_Type = models.ForeignKey(AddressType, on_delete=models.DO_NOTHING, related_name='Address_Type')
    address1 = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True, blank=True)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.Profile.user} Address'


class Product(InsertUpdate, models.Model):
    name = models.CharField(max_length=100)
    Product_Subcategory = models.ForeignKey(ProductSubcategory, on_delete=models.CASCADE, related_name='Product_Subcategory', null=True, blank=True)
    Product_Brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, related_name='Product_Brand', null=True, blank=True)
    Product_Unit_Type = models.ForeignKey(ProductUnitType, on_delete=models.CASCADE, related_name='Product_Unit_Type', null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    barcode = models.IntegerField(null=True, blank=True)
    image = models.ImageField(default='pics_default/default_product.jpg', upload_to=product_image_file_path)
    slug = models.SlugField(max_length=255, null=True, blank=True, default='')

    def __str__(self):
        return f'{self.name} Product'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Shop(InsertUpdate, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Shop_Category = models.ForeignKey(ShopCategory, on_delete=models.CASCADE, related_name='Shop_Category')
    name = models.CharField(max_length=100)
    Address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='Shop_Address')
    OpeningTime = models.CharField(max_length=100)
    ClosingTime = models.CharField(max_length=100)
    MinimumOrder = models.DecimalField(decimal_places=2, max_digits=10)
    MaximumOrder = models.DecimalField(decimal_places=2, max_digits=10)
    DeliveryCharges = models.DecimalField(decimal_places=2, max_digits=5)
    Shop_Status = models.ForeignKey(ShopStatus, on_delete=models.CASCADE, related_name='Shop_Status')
    slug = models.SlugField(max_length=255, null=True, blank=True, default='')

    def __str__(self):
        return f'{self.name} ({self.slug})'


class ShopProductCategory(InsertUpdate, models.Model):
    Shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='Shop_product')
    Product_Category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='Product_Category')
    slug = models.SlugField(max_length=255, null=True, blank=True, default='')

    def __str__(self):
        return f'{self.Shop}, {self.Product_Category}'


class ShopProduct(InsertUpdate, models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='Product')
    Shop_Product_Category = models.ForeignKey(ShopProductCategory, on_delete=models.CASCADE, related_name='Shop_Product_Category')
    Price = models.DecimalField(max_digits=8, decimal_places=2)
    slug = models.SlugField(max_length=255, null=True, blank=True, default='')

    def __str__(self):
        return f'{self.Product} Shop Product'


class Order(InsertUpdate, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')
    Total = models.DecimalField(max_digits=8, decimal_places=2)
    slug = models.SlugField(max_length=255, null=True, blank=True, default='')
    Order_Status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name='Order_Status')
    Note = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'{self.slug} Order'


class OrderShop(InsertUpdate, models.Model):
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='Order')
    Shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='Order_Shop')
    Items_Total = models.DecimalField(max_digits=8, decimal_places=2)
    DeliveryCharges = models.IntegerField()
    Note = models.TextField(max_length=100, null=True, blank=True)
    #Payment_Status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE, related_name='Payment_Status')
    #Payment = models.ForeignKey('Payment', on_delete=models.CASCADE, related_name='Payment', null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True, default='')

    def __str__(self):
        return f'{self.Order}Shop'


class OrderShopProduct(InsertUpdate, models.Model):
    Order_Shop = models.ForeignKey(OrderShop, on_delete=models.CASCADE, related_name='Order_Shop')
    Shop_Product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE, related_name='Shop_Products')
    Quantity = models.IntegerField()
    Weight = models.DecimalField(max_digits=5, decimal_places=2)
    Note = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.Shop_Product} {self.Order_Shop}'


class DriverOrder(InsertUpdate, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Driver_User')
    Driver_Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='Driver_Order')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user} {self.Driver_Order}'


class Payment(InsertUpdate, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_payment')
    Payment_Type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, related_name='Payment_Type')
    arrears = models.DecimalField(max_digits=8, decimal_places=2)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.DecimalField(max_digits=8, decimal_places=2)
    remaining = models.DecimalField(max_digits=8, decimal_places=2)
    create_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    paid_date = models.DateField()
    slug = models.SlugField(max_length=255, null=True, blank=True, default='')

    def __str__(self):
        return f'{self.slug} Payment'


class ServiceRequest(InsertUpdate, models.Model):
    location = models.CharField(max_length=200)
    Note = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'service request {self.id}'


def user_slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = utils.unique_slug_generator(instance, size=5)


def unique_slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = utils.unique_number_generator(instance, size=7)


pre_save.connect(user_slug_generator, sender=User)
pre_save.connect(unique_slug_generator, sender=Product)
pre_save.connect(unique_slug_generator, sender=Shop)
pre_save.connect(unique_slug_generator, sender=Order)
pre_save.connect(unique_slug_generator, sender=OrderShop)
pre_save.connect(unique_slug_generator, sender=Payment)
pre_save.connect(unique_slug_generator, sender=ProductCategory)
pre_save.connect(unique_slug_generator, sender=ShopProductCategory)
pre_save.connect(unique_slug_generator, sender=ShopProduct)


def create_profile(sender, instance, created, **kwargs):
    if created:
        print('im in create [rofile shabbers 1')
        print(instance)
        Profile.objects.create(user=instance)


def save_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_profile, sender=User)
post_save.connect(save_profile, sender=User)
