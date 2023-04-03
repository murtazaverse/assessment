from rest_framework import generics, permissions, status
from .models import Order
from .serializers import *
from .custom_permissions import IsOwner, IsOwnerOrSuperUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.http import HttpResponse
from django.contrib.auth.models import User

# studied JWT authentication in order to implement it in this assessment.
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.hashers import make_password

class CreateUser(APIView):

    """
    This API is used for creation of User.

    username = It must be unique, therefore, I have set phone_number here.
    first_name = First name of the user.
    last_name = Last name of the user.
    email = Email of that user.
    password = stores password in encrypted format.
    """

    def post(self, request, *args, **kwargs):
        user = User.objects.create(
            username = request.data.get('phone_number'),
            first_name = request.data.get('first_name'),
            last_name = request.data.get('last_name'),
            email = request.data.get('email'),
            password = make_password(request.data.get('password'))
        )

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "success":True,
                "refresh": str(refresh),
                "access": str(refresh.access_token)}, status=status.HTTP_200_OK)

        else:
            return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)

class ReadUpdateDeleteUsers(generics.GenericAPIView):

    """
    This API is used to fetch the User data.
    If any user_id is provided, the data would be fetched against that id, 
    otherwise,
    It would return all the users.
    """
    authentication_classes=[JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperUser] #ucl
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_users(self, user_id):

        """
        A function to fetch users against any ID.
        """

        try:
            user = User.objects.get(pk=user_id)
        except:
            user = None

        return user

    def get(self, request):

        """
        This call would fetch the users.
        If any user_id is passed in the query params, it would fetch user data against that id.
        otherwise,
        It would return all the users.
        """

        user_id = request.GET.get('user_id')
        user = request.user
        print("User isssss ===> ",user)
        
        if not user_id:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            return Response({"success":True, "users": serializer.data},
            status=status.HTTP_200_OK)

        else:
            user = self.get_users(user_id=user_id)
            if not user:
                return Response({
                    "success":False,
                    "message":"User against id : {id} does not exists".format(id=user_id)},
                    status=status.HTTP_400_BAD_REQUEST)

            if user.username == request.data.get('phone_number'):
                serializer = self.serializer_class(user)
                return Response({"success":True, "user": serializer.data},
                status=status.HTTP_200_OK)

            else:
                return Response(
                    {"success":False,
                    "message":"User not authorized"},
                    status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):

        """
        This function is used to update User data based on user_id.
        For this function, passing user_id is compulsory.
        """

        print('landed here')
        user_id = request.GET.get('user_id')
        user = self.get_users(user_id=user_id)
        if not user:
            return Response({
                "success":False,
                "message":"User against id : {id} does not exists".format(id=user_id)},
                status=status.HTTP_400_BAD_REQUEST)

        if user.username == request.data.get('phone_number'):
            serializer = self.serializer_class(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"success":True, "user": serializer.data},
                status=status.HTTP_200_OK)
            return Response({
                "success": False, 
                "message": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(
                {"success":False,
                "message":"User not authorized"},
                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        """
        This function is used to delete User data based on user_id.
        For this function, passing user_id is compulsory.
        """

        user_id = request.GET.get('user_id')
        user = self.get_users(user_id=user_id)
        if not user:
            return Response({
                "success":False,
                "message":"User against id : {id} does not exists".format(id=user_id)},
                status=status.HTTP_400_BAD_REQUEST)
        if user.username == request.data.get('phone_number'):
            user.delete()
            return Response(
                {"success":True,
                "message":"Data deleted successfully"},
                status=status.HTTP_200_OK)

        else:
            return Response(
                {"success":False,
                "message":"User not authorized"},
                status=status.HTTP_400_BAD_REQUEST)

class CreateOrders(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    """
    This API is used for creation of User.

    user = Would be fetched from Token.
    order_details = details of any order.
    order_total = total invoice amount of the order.
    """

    def post(self, request, *args, **kwargs):
        user = request.user

        order = Order.objects.create(
            user = user,
            order_details = request.data.get("details"),
            order_total = request.data.get("total")
        )

        if order:
            return Response({"success":True}, status=status.HTTP_200_OK)
        else:
            return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)

class ReadUpdateDeleteOrders(generics.GenericAPIView):

    """
    This API is used to fetch the Orders data.
    If any order_id is provided and the logged in user has place the order, only then the data 
    would be fetched against that id, 
    otherwise,
    It would return all the orders.
    """

    authentication_classes=[JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer 

    def get_order(self, order_id):
        try:
            order = Order.objects.get(pk=order_id)
        except:
            order = None

        return order

    def get(self, request):

        """
        This call would fetch the orders.
        If any order_id is passed in the query params, it would fetch order data against that id.
        otherwise,
        It would return all the orders.
        """

        order_id = request.GET.get('order_id')
        user = request.user
        if not order_id:
            order = Order.objects.filter(user=user)
            serializer = self.serializer_class(order, many=True)
            return Response({"success":True, "order": serializer.data},
            status=status.HTTP_200_OK)

        else:
            order = self.get_order(order_id=order_id)
            if not order:
                return Response({
                    "success":False,
                    "message":"Order against id : {id} does not exists".format(id=order_id)},
                    status=status.HTTP_400_BAD_REQUEST)

            if order.user == user:
                serializer = self.serializer_class(order)
                return Response({"success":True, "order": serializer.data},
                status=status.HTTP_200_OK)

            else:
                return Response(
                    {"success":False,
                    "message":"User not authorized"},
                    status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):

        """
        This function is used to update order data based on order_id.
        For this function, passing order_id is compulsory.
        """

        order_id = request.GET.get('order_id')
        order = self.get_order(order_id=order_id)
        user = request.user
        if not order:
            return Response({
                "success":False,
                "message":"Order against id : {id} does not exists".format(id=order_id)},
                status=status.HTTP_400_BAD_REQUEST)

        if order.user == user:
            serializer = self.serializer_class(
                order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"success":True, "order": serializer.data},
                status=status.HTTP_200_OK)
            return Response({
                "success": False, 
                "message": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(
                {"success":False,
                "message":"User not authorized"},
                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        """
        This function is used to delete order data based on order_id.
        For this function, passing order_id is compulsory.
        """

        order_id = request.GET.get('order_id')
        order = self.get_order(order_id=order_id)
        user = request.user
        if not order:
            return Response({
                "success":False,
                "message":"Order against id : {id} does not exists".format(id=order_id)},
                status=status.HTTP_400_BAD_REQUEST)
        if order.user == user:
            order.delete()
            return Response(
                {"success":True,
                "message":"Data deleted successfully"},
                status=status.HTTP_200_OK)

        else:
            return Response(
                {"success":False,
                "message":"User not authorized"},
                status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):

    """
    This API is used to login any user.
    It would provide Token for authentication.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(data)

class UserEmailList(generics.ListAPIView):

    """
    An API that returns the emails of all the Users.
    This would only work if the Logged In user is a Super User.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class OrderByUserEmail(generics.ListAPIView):

    """
    An API which will return all the orders against user emails.
    This would only work if the Logged In user is a Super User.
    """

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        emails = self.request.query_params.get('emails', '').split(',')
        users = User.objects.filter(email__in=emails)
        return Order.objects.filter(user__in=users)