# myapp/views.py
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from .models import Product,OrderedItem
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework import filters  # Import filters module for search functionality
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import CustomUserSerializer,ProductSerilizer,CustomTokenObtainPairSerializer,OrderedItemSerilizer,OrderSerlizer
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter


CustomUser = get_user_model()

@api_view(['GET'])
def api_root(request):
    return  Response({
        "products":reverse("list-product",request=request),
        "users":reverse("list-users",request=request),
        "orderdItems":reverse("list-OrderedItems",request=request)
    })

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


#creates a new user
class CustomUserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


#product list view
class ListProducts(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerilizer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

#shows each product
class ProductsDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerilizer
    lookup_field = 'id'  # This specifies that we are using 'id' as the lookup field


#shows all the users
class ListUsers(generics.ListAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=CustomUserSerializer


#shows a single user
class UserDetails(generics.RetrieveAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=CustomUserSerializer


class OrderedItemList(generics.ListCreateAPIView):
    queryset=OrderedItem.objects.all()
    serializer_class=OrderedItemSerilizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'user']

class OrderedItemsDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset=OrderedItem.objects.all()
    serializer_class=OrderedItemSerilizer
    lookup_field = 'id'  # This specifies that we are using 'id' as the lookup field




@api_view(['GET', 'POST'])
def Orders(request):
    if request.method == 'GET':
        user_id = request.query_params.get('user_id')
        if user_id:
            orders = OrderedItem.objects.filter(user=user_id)
           
        else:
            orders = OrderedItem.objects.all()
        serializer = OrderSerlizer(orders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderSerlizer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
