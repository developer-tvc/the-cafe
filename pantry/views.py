import json
import pymongo
import requests
import stripe

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from pprint import PrettyPrinter
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


from .forms import MenuForm, ContactForm
from .models import AboutCafe, Menu, Category, Cart, CartItem
from .serializers import GoogleAuthTokenSerializer
from .serializers import (
    CartItemsSerializer,
    ContactSerializer,
    GoogleAuthTokenSerializer,
    MenuSerializer,
    UpdateMenuSerializer,
)

stripe.api_key = settings.STRIPE_SECRET_KEY
printer = PrettyPrinter()

User = get_user_model()


class GoogleAuthAPIView(APIView):
    """GoogleAuthAPIView handles the authentication of users through Google OAuth.

    This view is responsible for:

    - Receiving a Google OAuth token (or authorization code) from the client.
    - Validating the token with Google's OAuth2 service.
    - Creating or retrieving a user in the local Django database based on the Google account information.
    - Returning an authentication token or a session for use in subsequent API requests.

    HTTP Methods:
    -------------
    - POST: Accepts the Google OAuth token, validates it, and returns a response with the user
      authentication token or an error message.

    Methods:
    --------
    - post(request, *args, **kwargs): Handles the POST request to authenticate a user with Google OAuth.

    Dependencies:
    -------------
    - google-auth: A third-party package used to verify the Google OAuth token.
    - rest_framework: Django Rest Framework for API view handling and response formatting.
    """

    def post(self, request, *args, **kwargs):
        try:
            serializer = GoogleAuthTokenSerializer(data=request.data)
            if serializer.is_valid():
                access_token = serializer.validated_data["access_token"]

                # Get user info from Google
                user_info_response = requests.get(
                    settings.SOCIAL_REST_GOOGLE_OAUTH2_URL,
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                if user_info_response.status_code == 200:
                    user_info = user_info_response.json()
                    # Authenticate or create the user
                    user, created = User.objects.get_or_create(
                        email=user_info["email"],
                        defaults={"username": user_info["name"]},
                    )
                    # Optionally update user info here if needed
                    if created:
                        pass  # Handle any additional user setup here
                    # Return user data or any other response
                    return Response(
                        {"user": {"username": user.username, "email": user.email}},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"error": "Failed to fetch user info"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            return Response(
                {"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e)


class CafeHome(TemplateView):
    """
    Landing home page view,

    - Used for showcase the landing page elements
    - Such as contact form ,menu items, ordering facility
      and search facility of food items
    - Exception handling implemented

    """

    template_name = "cafe.html"
    form = ContactForm()

    def get_context_data(self, **kwargs):
        try:
            cafe = AboutCafe.objects.all().first()
            menus = Menu.objects.values(
                "id",
                "dish_name",
                "dish_photo",
                "category_name",
                "dish_discription",
                "dish_price",
                "approval_flag",
            )
            context = super().get_context_data(**kwargs)
            context["cafe"] = cafe
            context["menus"] = menus
            context["form"] = self.form
            print(context)
            return context
        except Exception as e:
            print(e)
            return HttpResponseRedirect("something_went_wrong.html")


# Menu
class CafeMenu(APIView):
    """
    Cafe food menu view used for display items and add new items
    - login authentication permission implemented
    - Exception handling implemented.

    Methods:
    --------
    - get(self, request)- method used for showcase menu items by checking login user is superuser or not.
    - post(self, request)- method used for adding new menu items using by HTML form from client side.

    """

    renderer_classes = [TemplateHTMLRenderer]
    permissions = [permissions.IsAuthenticated]
    template_name = "suggestion_menu.html"
    form = MenuForm()

    def get(self, request):
        try:
            if self.request.user.is_superuser:
                menus = Menu.objects.all()
            else:
                menus = Menu.objects.values(
                    "dish_name",
                    "dish_photo",
                    "dish_discription",
                    "dish_price",
                    "approval_flag",
                )
            return render(
                request, self.template_name, {"form": self.form, "menus": menus}
            )
        except Exception as e:
            print(e)
            return render(request, "something_went_wrong.html")

    def post(self, request):
        try:
            if not request.POST._mutable:
                request.POST._mutable = True
                caf = AboutCafe.objects.all().first()
                print(caf.id)
                cat = request.POST.get("category")
                c_name = Category.objects.get(id=cat)
                
                request.data["cafe"] = caf.id
                request.data["category_name"] = c_name.category_name
            serializer = MenuSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                menus = Menu.objects.all()
                return render(
                    request, self.template_name, {"form": self.form, "menus": menus}
                )
            else:
                return render(request, "something_went_wrong.html")
        except Exception as e:
            print(e)
            return render(request, "something_went_wrong.html")


class UpdateCafeMenu(APIView):
    """
    Cafe food menu view used for update items and approve items
    - login authentication permission implemented
    - Exception handling implemented.

    Methods:
    --------
    - post(self, request, *args, **kwargs)- method used for updating existing menu item's
                                            price and approval flag using by check box from
                                            client side based on id.
    - delete((self, request, id, *args, **kwargs)) - method used for deleting existing menu items using id.

    """

    renderer_classes = [TemplateHTMLRenderer]
    permissions = [permissions.IsAuthenticated]
    template_name = "suggestion_menu.html"
    form = MenuForm()

    def post(self, request, *args, **kwargs):
        try:
            if not request.POST._mutable:
                request.POST._mutable = True
                if request.data["approval_flag"] == "on":
                    request.data["approval_flag"] = True
                else:
                    request.data["approval_flag"] = False
            request.POST._mutable = False
            initial_data = request.data
            menu_id = request.data["id"]
            menu = Menu.objects.get(id=menu_id)
            serializer = UpdateMenuSerializer(data=initial_data)
            if serializer.is_valid():
                menus = Menu.objects.all()
                serializer.update(menu, initial_data)
                return render(
                    request, self.template_name, {"form": self.form, "menus": menus}
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return render(request, "something_went_wrong.html")

    def delete(self, request, id, *args, **kwargs):
        try:
            menu_id = int(id)
            menu = Menu.objects.get(id=menu_id)
            deleted = menu.delete()
            if deleted:
                menus = Menu.objects.all()
                return render(
                    request, self.template_name, {"form": self.form, "menus": menus}
                )
            else:
                return Response(request, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return render(request, "something_went_wrong.html")


class CafeContact(APIView):
    """Contact view used for send/recevie contact messages from customers

    Methods:
    --------
    - get(self, request)- method used for display form and accept messages.
    - post(self, request)- method used for sending messages from customers using HTML client form.
    - Exception handling implemented

    """

    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]
    template_name = "cafe.html"
    form = ContactForm()

    def get(self, request):
        try:
            cafe = AboutCafe.objects.all().first()
            menus = Menu.objects.values(
                "id",
                "dish_name",
                "dish_photo",
                "category_name",
                "dish_discription",
                "dish_price",
                "approval_flag",
            )
            return render(
                request,
                self.template_name,
                {"form": self.form, "menus": menus, "cafe": cafe},
            )
        except Exception as e:
            print(e)
            return render(request, "something_went_wrong.html")

    def post(self, request):
        try:
            serializer = ContactSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                cafe = AboutCafe.objects.all().first()
                menus = Menu.objects.values(
                    "id",
                    "dish_name",
                    "dish_photo",
                    "category_name",
                    "dish_discription",
                    "dish_price",
                    "approval_flag",
                )
                return render(
                    request,
                    self.template_name,
                    {"form": self.form, "menus": menus, "cafe": cafe},
                )
            else:
                return HttpResponse("Could not save data")
        except Exception as e:
            print(e)
            return render(request, "something_went_wrong.html")


class SearchCafeMenu(APIView):
    """View used for search the menu items and display search results.
        - Here the seach functionality implemented using mongo db's text indexing.
        - We can search using category and dish names.
        - It will display the dishes based on seach query.

    - Exception handling implemented

    Methods:
    --------
    - get(self, request)- method used for accept the search query and display list of results based on it.

    Dependencies:
    -------------
    - Mongo db - Mongo db connection with django, connected in settings.py
               - Text indexing in mongo db.
    - pprint - used for displaying results in command prompt.

    """

    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]
    template_name = "search_results.html"

    try:
        # Mongo DB connection
        myclient = pymongo.MongoClient(settings.DATABASE_CONNECTION)
        db = myclient.mymongo_db
        # Collection Object
        collection = db.pantry_menu

        def get(self, request):
            my_search = request.GET.get("search")
            result = self.collection.find({"$text": {"$search": my_search}})
            result = list(result)
            printer.pprint(list(result))
            return render(
                request, self.template_name, {"result": result, "search": my_search}
            )

    except Exception as e:
        print(e)


class CreateCheckoutSessionView(View):
    """
    Payment Gateway Stripe used for stripe payments
    - View used for doing payments using stripe payment gateway.
    - Using stripe checkout session requests and response json the payment url will generate.
    - Redirecting url will display the payment gateway connecting with the merchent's payment account.
    - We can do payments there using debit/credit cards
    - Test stripe account used for do the dummy payments.

    - login authentication permission implemented
    - Exception handling implemented

    Methods:
    --------
    - post(self, request,*args,**kwargs)- method used for accept the connection request with stripe and generate
                                          checkout session json which redirecting to payment gate way url.
    Dependencies:
    -------------
    - Stripe - stripe connection which connected using keys from imported in settings.py
    - pprint - used for displaying results in command prompt.

    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            YOUR_DOMAIN = settings.CAFE_DOMAIN
            dish = Menu.objects.get(id=self.kwargs["id"])
            dish_price = int(dish.dish_price * 100)
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": dish.dish_name,
                                "description": "the Cafe",
                                "images": [settings.STRIPE_CAFE_IMAGE],
                            },
                            "unit_amount": dish_price,
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=YOUR_DOMAIN + "success/",
                cancel_url=YOUR_DOMAIN + "cancel/",
            )
            return redirect(checkout_session.url)

        except Exception as e:
            print(e)
            return render(request, "something_went_wrong.html")


# login view
def login(request):
    """login html view"""
    return render(request, "login.html")


# success view
def success(request):
    """success html view"""
    return render(request, "success.html")


# cancel view
def cancel(request):
    """cancel html view"""
    return render(request, "cancel.html")


# something went wrong view
def something_went_wrong(request):
    """something went wrong html view"""
    return render(request, "something_went_wrong.html")


@csrf_exempt
def stripe_webhook(request):
    """
    Stripe webhook used for catching payment events and take appropriate actions
    - View used for handling paymentevents using stripe payment gateway.
    - Uses input as json response from stripe checkout session function
    - Can handle multiple payment events, here, only used payment intent succeeded.
    - Exception handling implemented

    Dependencies:
    -------------
    - Stripe - stripe connection which connected using keys from imported in settings.py
             - json response from stripe checkout session.
             - stripe webhook used for catch and take action based on events

    """
    payload = json.loads(request.body)
    sig_hader = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_hader, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        print(e)
        # Invalied payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalied signature
        return HttpResponse(status=400)
    print(event)
    # Handle the checkout.session.completed event'
    try:
        if event["type"] == "payment_intent.succeeded":
            session = event["data"]["object"]
            print(session)
        return HttpResponse(status=200)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=e)


class CartView(APIView):
    """ "
    Shopping cart API view used for single
    - item purchase,
    - calculate price of single item
    - update items and
    - delete items

    Methods:
    --------
    - get(self, request)- method used for display cart items and total.
    - post(self, request)-method used for add cart items based on quantity  and calculate total price.
    - put(self,request) - method used for update  selected cart items based on quanitity and calaculate price
                          based on updated cart items and quanitity.
    - delete(self,request) -method used for delete selectecd cart items and calaculate new price based on updates.

    - Exception handling implemented

    Dependencies:
    -------------
    - Model cartItem - All the above mentioned operations done at pre_save method of Model.
    - Model cart - cart for indiviual user and  items and price saved here.

    """

    permission_classes = [
        AllowAny,
    ]

    # Show Cart Items
    def get(self, request):
        try:
            user = request.user
            cart_item = Cart.objects.filter(user=user, orderd=False).first()
            print(cart_item)
            query_set = CartItem.objects.filter(cart=cart_item)

            serializer = CartItemsSerializer(query_set, many=True)
            print(serializer.data)
            return Response(
                {"success": "Permission Working", "Cart Items": serializer.data}
            )
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e)

    # Add Cart Items
    def post(self, request):
        data = request.data
        user = request.user
        cart_item, _ = Cart.objects.get_or_create(user=user, orderd=False)
        try:
            menu_item = Menu.objects.get(id=data.get("menu_item"))
            price = menu_item.dish_price
            quantity = data.get("quantity")
            cart_items = cartItem(
                cart=cart_item,
                user=user,
                product=menu_item,
                price=price,
                quantity=quantity,
            )
            cart_items.save()
            total_price = 0
            cart_items = CartItem.objects.filter(user=user, cart=cart_item.id)
            for items in cart_items:
                total_price += items.price
            cart_item.total_price = total_price
            cart_item.save()
        except menu_item.DoesNotExist:
            pass
        return Response({"Success": "Items added to your Cart"})

    # Update Cart Items
    def put(self, request):
        data = request.data
        user = request.user
        try:
            cart_item = CartItem.objects.get(id=data.get("id"))
            quantity = int(data.get("quantity"))
            cart_item.quantity += quantity
            cart_item.save()

            cart_item_new, _ = cart.objects.get_or_create(user=user, orderd=False)
            total_price = 0
            cart_items = CartItem.objects.filter(user=user, cart=cart_item_new.id)
            for items in cart_items:
                total_price += items.price
            cart_item_new.total_price = total_price
            cart_item_new.save()

            my_cart = Cart.objects.filter(user=user, orderd=False).first()
            query_set = CartItem.objects.filter(cart=my_cart)
            serializer = CartItemsSerializer(query_set, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e)

    # Delete Cart Items
    def delete(self, request):
        data = request.data
        user = request.user
        try:
            cart_item = CartItem.objects.get(id=data.get("id"))
            cart_item.delete()
            cart_item_new, _ = Cart.objects.get_or_create(user=user, orderd=False)
            total_price = 0
            cart_items = CartItem.objects.filter(user=user, cart=cart_item_new.id)
            for items in cart_items:
                total_price += items.price
            cart_item_new.total_price = total_price
            cart_item_new.save()
            my_cart = Cart.objects.filter(user=user, orderd=False).first()
            query_set = CartItem.objects.filter(cart=my_cart)
            serializer = CartItemsSerializer(query_set, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e)
