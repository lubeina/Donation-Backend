from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Donation,Restaurant,Menu, DonationBasket
from datetime import date


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password'] #'phone']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        # phone = validated_data['phone']
        new_user = User(username=username, first_name=first_name,
                        last_name=last_name, email=email) #phone=phone)
        new_user.set_password(password)
        new_user.save()
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileSerializer(serializers.ModelSerializer):
    past_donations = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'past_donations'] #, 'phone'

    def get_past_donations(self, obj):
        amount = Donation.objects.filter(user=obj, date__lte=date.today(), active=False)
        return DonationSerializer(amount, many=True).data

class RestaurantProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['name','location', 'description', 'image','id']


class DonationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Donation
        fields = ['amount', 'user', 'active', 'id', 'date']

class RestaurantSerializer(serializers.ModelSerializer):
    menu_total = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ['name', 'location', 'description', 'image','id','menu_total']
    
    def get_menu_total(self,obj):
        menu_total = 0
        menu_items = Menu.objects.filter(restaurant=obj.id)
        for item in menu_items:
            menu_total+=item.total
        return menu_total



class MenuSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id','name', 'original_price', 'discount','discounted_price','description','available_qty','total','restaurant']

    def get_discounted_price(self, obj):
        return obj.original_price*((100-obj.discount)/100)
    
    def get_total(self, obj):
        return (obj.original_price*((100-obj.discount)/100))*obj.available_qty

class MenuAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id','name', 'original_price', 'discount','description','available_qty']
    
class MenuUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['available_qty']

class RestaurantDetailSerializer(serializers.ModelSerializer):
    menu = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ['name', 'location', 'description', 'image','id','menu']

    def get_menu(self,obj):
        menu = Menu.objects.filter(restaurant=obj.id)
        return MenuSerializer(menu, many=True).data

class DonationBasketAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationBasket
        fields = []

class DonationBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationBasket
        fields = ['restaurant', 'date', 'single_restaurant_total', 'total_donation_recieved','id']


