from rest_framework import serializers

from .models import AboutCafe, Cart, CartItem, Contact, Menu


class GoogleAuthTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()


class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutCafe
        fields = ["__all__"]


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "cafe",
            "category",
            "category_name",
            "dish_name",
            "dish_discription",
            "dish_photo",
        ]


class UpdateMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["dish_price", "approval_flag"]

        def update(self, instance, validated_data):

            instance.dish_price = validated_data.get("dish_price", instance.dish_price)
            instance.approval_flag = validated_data.get(
                "approval_flag", instance.approval_flag
            )
            instance.save()
            return instance


class UserSerializer(serializers.Serializer):
    first_name = serializers.EmailField()
    last_name = serializers.EmailField()
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["name", "number_of_People", "date_of_booking", "message", "phone_no"]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class CartItemsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    cart = CartSerializer()
    product = MenuSerializer()

    class Meta:
        model = CartItem
        fields = ["cart", "user", "product", "price", "quantity"]
