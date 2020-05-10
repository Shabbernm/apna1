import requests
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.db.models import Q

from . import models, serializers, imp_functions, merge


def home(request):
    return render(request, '')


def test(request):
    return render(request, 'core/test.html')


def GetG(request):
    r = requests.post('http://127.0.0.1:8000/core/gender/', data=request.GET)
    print(r)
    return render(request, 'core/test.html')


class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system """
    serializer_class = serializers.UserSerializer


class CreateTokenView(ObtainAuthToken):
    """ Create a new token for user """
    serializer_class = serializers.AuthTokeSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)


class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        # print('User of a request is: '+request.user)
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Manage the authenticated user """
    serializer_class = serializers.UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """ Retrieve and return authenticated user """
        return self.request.user


class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ShopSerializer
    queryset = models.Shop.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        responseData = []
        # print('User ID is: ' + str(self.request.user.id))
        shopCategoryId = self.request.GET.get('shopCategoryId')
        if shopCategoryId is not None:
            data = self.queryset.filter(Shop_Category=shopCategoryId)
        else:
            data = self.queryset.filter(user__id=self.request.user.id)
        print('data')
        # print(data[0].Shop_Category.Name)
        # responseData.append(data)
        # if(data[0].Shop_Category.Name=='Grocery Shop'):
        #     print('Its a grocery shop so add shop product category data')
        #     responseData.append(models.ShopProductCategory.objects.filter(Shop__user__id=self.request.user.id))
        # print(responseData)
        return data

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return serializers.ShopAddSerializer
        return serializers.ShopSerializer


class ShopByLocationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ShopSerializer
    queryset = models.Shop.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        shopList = []
        tempList = []
        # print('User ID is: ' + str(self.request.user.id))
        shopCategoryId = self.request.GET.get('shopCategoryId')
        latitude = self.request.GET.get('latitude')
        longitude = self.request.GET.get('longitude')
        distance = self.request.GET.get('distance')

        # Address__location is a string
        # get long and lat
        # then match location and get nearby shops
        # Active
        data = self.queryset.filter(Q(Shop_Category=shopCategoryId) & Q(Shop_Status__Name='Active'))
        # category filtered shops
        # get nearby shops by long and lat
        for item in data:
            locationList = item.Address.location.split('_')
            print(locationList[0])
            print(locationList[1])
            check = imp_functions.getNearbyShops(float(latitude), float(longitude), float(locationList[0]), float(locationList[1]), float(distance))
            if check:
                # add in list
                itemList = []
                itemList.append(item)
                # shopList.append(item)
                dist = imp_functions.getNearbyShopDistance(float(latitude), float(longitude), float(locationList[0]), float(locationList[1]))
                print('dist')
                print(dist)

                itemList.append(dist)
                tempList.append(itemList)

        # sort by distance
        # imp_functions.sortShopList(shopList, distanceList)
        print('before')
        print(shopList)
        print('shopList')
        print(tempList)
        tempList = merge.mergeSort(tempList)
        print(tempList)
        shopList = []
        for item in tempList:
            shopList.append(item[0])
        print('after')
        print(shopList)

        # print('data')
        # print(data[0].Shop_Category.Name)
        # responseData.append(data)
        # if(data[0].Shop_Category.Name=='Grocery Shop'):
        #     print('Its a grocery shop so add shop product category data')
        #     responseData.append(models.ShopProductCategory.objects.filter(Shop__user__id=self.request.user.id))
        # print(responseData)
        return shopList

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return serializers.ShopAddSerializer
        return serializers.ShopSerializer


class ShopProductCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ShopProductCategorySerializer
    queryset = models.ShopProductCategory.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        print('User ID is: ' + str(self.request.user.id))
        shopId = self.request.GET.get('shopId')
        return self.queryset.filter(Shop=shopId)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ShopProductCategoryAddSerializer
        return serializers.ShopProductCategorySerializer


class CityViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CitySerializer
    queryset = models.City.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(Is_Active=True)


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class ShopCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ShopCategorySerializer
    queryset = models.ShopCategory.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(Is_Active=True)


class ShopStatusViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ShopStatusSerializer
    queryset = models.ShopStatus.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(Is_Active=True)


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AddressSerializer
    queryset = models.Address.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(Profile__user__id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return serializers.AddressAddSerializer
        return serializers.AddressSerializer


class AddressTypeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AddressTypeSerializer
    queryset = models.AddressType.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileSerializer
    queryset = models.Profile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user__id=self.request.user.id)


class GenderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GenderSerializer
    queryset = models.Gender.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class ProfileStatusViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileStatusSerializer
    queryset = models.ProfileStatus.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class ProductCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductCategorySerializer
    queryset = models.ProductCategory.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        shopCategoryId = self.request.GET.get('shopCategoryId')
        print(shopCategoryId)
        return self.queryset.filter(Q(Is_Active=True) & Q(Shop_Category=shopCategoryId)).order_by('Name')


class ProductUnitTypeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductUnitTypeSerializer
    queryset = models.ProductUnitType.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class ProductBrandViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductBrandSerializer
    queryset = models.ProductBrand.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class OrderStatusViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderStatusSerializer
    queryset = models.OrderStatus.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class ProductSubcategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSubcategorySerializer
    queryset = models.ProductSubcategory.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        shopCategoryId = self.request.GET.get('shopCategoryId')
        return self.queryset.filter(Product_Category__Shop_Category=shopCategoryId)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        productSubcategoryId = self.request.GET.get('productSubcategoryId')
        return self.queryset.filter(Product_Subcategory=productSubcategoryId)


class ShopProductViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ShopProductSerializer
    queryset = models.ShopProduct.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        shopId = self.request.GET.get('shopId')
        shopProductsCategoryId = self.request.GET.get('shopProductsCategoryId')
        if shopProductsCategoryId is not None:
            data = self.queryset.filter(Shop_Product_Category=shopProductsCategoryId)
        else:
            data = self.queryset.filter(Shop_Product_Category__Shop=shopId)
        return data

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'create':
            return serializers.ShopProductAddSerializer
        return serializers.ShopProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer
    queryset = models.Order.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        getShopOrders = self.request.GET.get('getShopOrders')
        if getShopOrders is not None:
            pass
            # today 20 orders
            # orderShopQuery = models.OrderShop.objects.filter(Shop__user__id=self.request.user.id).values('Order')
            # orderShopQuery.
            data = self.queryset.filter(id__in=models.OrderShop.objects.filter(Shop__user__id=self.request.user.id).values('Order'))
        else:
            data = self.queryset.filter(user__id=self.request.user.id)
        return data

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'create' or self.action == 'partial_update':
            return serializers.OrderAddSerializer
        return serializers.OrderSerializer


class OrderShopViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderShopSerializer
    queryset = models.OrderShop.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(Order__user__id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'create':
            return serializers.OrderShopAddSerializer
        return serializers.OrderShopSerializer


class OrderShopProductViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderShopProductSerializer
    queryset = models.OrderShopProduct.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        todayOrders = self.request.GET.get('todayOrders')
        orderId = self.request.GET.get('orderId')
        if todayOrders is not None:
            # today 20 orders
            # data = ''
            # data = self.queryset.filter(Order_Shop__Shop__user__id=self.request.user.id).order_by('-Inserted_On')[:float(todayOrders)]
            data = self.queryset.filter(Order_Shop__Order__id=orderId).order_by('-Inserted_On')[:float(todayOrders)]
            print('data')
            print(data)
        else:
            data = self.queryset.filter(Order_Shop__Order__user__id=self.request.user.id)
        return data

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'create':
            return serializers.OrderShopProductAddSerializer
        return serializers.OrderShopProductSerializer


class ServiceRequestViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ServiceRequestSerializer
    queryset = models.ServiceRequest.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()