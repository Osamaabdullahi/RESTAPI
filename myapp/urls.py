from django.urls import path 
from . import views


urlpatterns=[
    path("",views.api_root),
    path("products/",views.ListProducts.as_view(),name="list-product"),
    path("products/<uuid:id>/",views.ProductsDetails.as_view(),name="product-details"),
    path("users/",views.ListUsers.as_view(),name="list-users"),
    path("users/<int:pk>/",views.UserDetails.as_view(),name="users-details"),
    path('api/register/', views.CustomUserCreate.as_view(), name='create_user'),
    path("orderditems/",views.OrderedItemList.as_view(),name="list-OrderedItems"),
    path("orderditems/<uuid:id>/",views.OrderedItemsDetails.as_view(),name="OrderedItems-details"),
    path("orders/",views.Orders,name="orders")

]