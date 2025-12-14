from .models import (UserProfile,Category,Store,Contact,Address,StoreMenu,
                     Product,Order,Courier,Review)
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','first_name',]


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name',]


class StoreListSerializer(serializers.ModelSerializer):
    created_date = serializers.DateField(format='%d-%m-%Y')
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()
    avg_procent = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['id','store_name','store_image','created_date','avg_rating','count_people','avg_procent']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()

    def get_avg_procent(self, obj):
        return obj.get_avg_procent()


class StoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category_name']

class CategoryStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']



class CategoryDetailSerializer(serializers.ModelSerializer):
    category_store = StoreListSerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ['category_name','category_store']




class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['contact_name','contact_number']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name','product_image','product_price','product_description']


class StoreMenuListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreMenu
        fields = ['id','menu_name']


class StoreMenuDetailSerializer(serializers.ModelSerializer):
    menu_store = ProductSerializer(many=True,read_only=True)
    class Meta:
        model = StoreMenu
        fields = ['menu_name','menu_store']



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'



class OrderStatusSerializer(serializers.ModelSerializer):
    products = ProductSerializer()
    client = UserProfileListSerializer()
    class Meta:
        model = Order
        fields = ['id','products','client','status']



class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'



class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'



class ReviewSerializer(serializers.ModelSerializer):
    client = UserProfileNameSerializer()
    created_at = serializers.DateTimeField(format='%d-%m-%Y')
    class Meta:
        model = Review
        fields = ['client','rating','text','created_at','courier']


class StoreDetailSerializer(serializers.ModelSerializer):
    created_date = serializers.DateField(format='%d-%m-%Y')
    category = CategoryStoreSerializer()
    owner = UserProfileNameSerializer()
    contact_store = ContactSerializer(many=True,read_only=True)
    address_store = AddressSerializer(many=True,read_only=True)
    store_menu_store = StoreMenuDetailSerializer(many=True,read_only=True)
    review_store = ReviewSerializer(many=True,read_only=True)
    class Meta:
        model = Store
        fields = ['store_name','store_image','description','category','owner','created_date',
                  'contact_store','address_store','store_menu_store','review_store']



