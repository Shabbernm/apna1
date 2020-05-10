from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'core'

router = routers.DefaultRouter()
router.register('allShops', views.ShopViewSet)
router.register('getShopsByLocation', views.ShopByLocationViewSet)
router.register('productCategory', views.ProductCategoryViewSet)
router.register('shopProductCategory', views.ShopProductCategoryViewSet)
router.register('city', views.CityViewSet)
router.register('country', views.CountryViewSet)
router.register('shopCategory', views.ShopCategoryViewSet)
router.register('shopStatus', views.ShopStatusViewSet)
router.register('address', views.AddressViewSet)
router.register('addressType', views.AddressTypeViewSet)
router.register('profile', views.ProfileViewSet)
router.register('gender', views.GenderViewSet)
router.register('profileStatus', views.ProfileStatusViewSet)
router.register('productUnitType', views.ProductUnitTypeViewSet)
router.register('productBrand', views.ProductBrandViewSet)
router.register('productSubcategory', views.ProductSubcategoryViewSet)
router.register('product', views.ProductViewSet)
router.register('shopProduct', views.ShopProductViewSet)
router.register('order', views.OrderViewSet)
router.register('orderShop', views.OrderShopViewSet)
router.register('orderStatus', views.OrderStatusViewSet)
router.register('orderShopProduct', views.OrderShopProductViewSet)
router.register('serviceRequest', views.ServiceRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('home/', views.home, name='home'),
    path('test/', views.test, name='test'),
    path('GetG/', views.GetG, name='GetG'),

    path('signup/', views.CreateUserView.as_view(), name='signup'),
    path('login/', views.CreateTokenView.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='Logout'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]