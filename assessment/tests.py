import json
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Order
from .serializers import OrderSerializer, UserSerializer
# from django.test import TestCase, Client

