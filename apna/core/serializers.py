from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from . import models


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the users object """

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'user_type', 'slug')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """ Create a new user with encrypted password and return it"""
        print(validated_data)
        return get_user_model().objects.create_type_user(**validated_data)

    def update(self, instance, validated_data):
        """ Update a user, setting the password correctly and return it """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokeSerializer(serializers.Serializer):
    """ Serializer for the user authentication object """
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """ Validate and authenticate the user """
        email = attrs.get('email')
        password = attrs.get('password')
        print('self.context.get(request)')
        print(self.context.get('request'))
        print('attrs')
        print(attrs)

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = ('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        # print('User from authentication: ' + str(user))
        attrs['user'] = user
        return attrs

    class Meta:
        model = models.User
        fields = ['id', 'email', 'user']


class ShopCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShopCategory
        fields = ['id', 'Name', 'Description', 'image',
                  'Is_Active', 'System_Used', 'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = ['id', 'Name', 'Description',
                  'Is_Active', 'System_Used', 'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class CitySerializer(serializers.ModelSerializer):
    countryy = CountrySerializer(many=False)

    class Meta:
        model = models.City
        fields = ['id', 'Name', 'Description', 'countryy',
                  'Is_Active', 'System_Used', 'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class AddressTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AddressType
        fields = ['id', 'Name', 'Description',
                  'Is_Active', 'System_Used', 'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer(many=False)
    Address_Type = AddressTypeSerializer(many=False)

    class Meta:
        model = models.Address
        fields = ['id', 'Profile', 'Address_Type', 'address1', 'city', 'location',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class AddressAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ['id', 'Profile', 'Address_Type', 'address1', 'city', 'location',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class ShopStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShopStatus
        fields = ['id', 'Name', 'Description',
                  'Is_Active', 'System_Used', 'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class ShopSerializer(serializers.ModelSerializer):
    Shop_Category = ShopCategorySerializer(many=False)
    Address = AddressSerializer(many=False)
    Shop_Status = ShopStatusSerializer(many=False)

    class Meta:
        model = models.Shop
        fields = ['id', 'user', 'Shop_Category', 'name', 'Address', 'OpeningTime', 'ClosingTime', 'MinimumOrder',
                  'MaximumOrder', 'DeliveryCharges', 'Shop_Status', 'slug',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class ShopAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shop
        fields = ['id', 'user', 'Shop_Category', 'name', 'Address', 'OpeningTime', 'ClosingTime', 'MinimumOrder',
                  'MaximumOrder', 'DeliveryCharges', 'Shop_Status', 'slug',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = ['id', 'Name', 'Description', 'Shop_Category', 'image', 'slug',
                  'Is_Active', 'System_Used', 'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class ShopProductCategorySerializer(serializers.ModelSerializer):
    Shop = ShopSerializer(many=False)
    Product_Category = ProductCategorySerializer(many=False)

    class Meta:
        model = models.ShopProductCategory
        fields = ['id', 'Shop', 'Product_Category', 'slug',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class ShopProductCategoryAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShopProductCategory
        fields = ['id', 'Shop', 'Product_Category', 'slug',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gender
        fields = ['id', 'Name', 'Description',
                  'Is_Active', 'System_Used', 'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class ProfileStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfileStatus
        fields = ['id', 'Name', 'Description',
                  'Is_Active', 'System_Used', 'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class ProfileSerializer(serializers.ModelSerializer):
    gender = GenderSerializer(many=False)
    city = CitySerializer(many=False)
    country = CountrySerializer(many=False)
    Profile_Status = ProfileStatusSerializer(many=False)

    class Meta:
        model = models.Profile
        fields = ['id', 'user', 'gender', 'Full_Name', 'CNIC', 'DOB', 'contact', 'other_contacts', 'city',
                  'country', 'WhatsApp', 'Profile_Status', 'image',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']

        class ProductBrandSerializer(serializers.ModelSerializer):
            Product_Category = ProductCategorySerializer(many=False)

            class Meta:
                model = models.ProductBrand
                fields = ['id', 'Name', 'Description', 'Product_Category',
                          'Is_Active', 'System_Used', 'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class ProductUnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductUnitType
        fields = ['id', 'Name', 'Description',
                  'Is_Active', 'System_Used', 'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class ProductBrandSerializer(serializers.ModelSerializer):
    Product_Category = ProductCategorySerializer(many=False)

    class Meta:
        model = models.ProductBrand
        fields = ['id', 'Name', 'Description', 'Product_Category',
                  'Is_Active', 'System_Used', 'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class ProductSubcategorySerializer(serializers.ModelSerializer):
    Product_Category = ProductCategorySerializer(many=False)

    class Meta:
        model = models.ProductSubcategory
        fields = ['id', 'Name', 'Description', 'Product_Category',
                  'Is_Active', 'System_Used', 'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class ProductSerializer(serializers.ModelSerializer):
    Product_Subcategory = ProductSubcategorySerializer(many=False)
    Product_Brand = ProductBrandSerializer(many=False)
    Product_Unit_Type = ProductUnitTypeSerializer(many=False)

    class Meta:
        model = models.Product
        fields = ['id', 'name', 'Product_Subcategory', 'Product_Brand', 'Product_Unit_Type', 'description',
                  'barcode', 'image', 'slug',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class ShopProductSerializer(serializers.ModelSerializer):
    Product = ProductSerializer(many=False)
    Shop_Product_Category = ShopProductCategorySerializer(many=False)

    class Meta:
        model = models.ShopProduct
        fields = ['id', 'Product', 'Shop_Product_Category', 'Price', 'slug',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class ShopProductAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShopProduct
        fields = ['id', 'Product', 'Shop_Product_Category', 'Price', 'slug',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderStatus
        fields = ['id', 'Name', 'Description',
                  'Is_Active', 'System_Used', 'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class OrderSerializer(serializers.ModelSerializer):
    Order_Status = OrderStatusSerializer(many=False)

    class Meta:
        model = models.Order
        fields = ['id', 'user', 'Total', 'slug', 'Order_Status', 'Note',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class OrderAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['id', 'user', 'Total', 'slug', 'Order_Status','Note',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class OrderShopSerializer(serializers.ModelSerializer):
    Order = OrderSerializer(many=False)
    Shop = ShopSerializer(many=False)

    class Meta:
        model = models.OrderShop
        fields = ['id', 'Order', 'Shop', 'Items_Total', 'DeliveryCharges', 'Note', 'slug',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class OrderShopAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderShop
        fields = ['id', 'Order', 'Shop', 'Items_Total', 'DeliveryCharges', 'Note', 'slug',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class OrderShopProductSerializer(serializers.ModelSerializer):
    Order_Shop = OrderShopSerializer(many=False)
    Shop_Product = ShopProductSerializer(many=False)

    class Meta:
        model = models.OrderShopProduct
        fields = ['id', 'Order_Shop', 'Shop_Product', 'Quantity', 'Weight', 'Note',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class OrderShopProductAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderShopProduct
        fields = ['id', 'Order_Shop', 'Shop_Product', 'Quantity', 'Weight', 'Note',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceRequest
        fields = ['id', 'location', 'Note',
                  'Inserted_By', 'Inserted_On', 'Updated_By', 'Updated_On']