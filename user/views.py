from rest_framework.decorators import APIView
from django.http import JsonResponse
import base64
import logging
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.authtoken.models import Token
from app import global_code
from django.db import transaction
from .models import UserBalance
from django.contrib.auth import authenticate

logger = logging.getLogger('django')
def login_data(request):
    error_list= []
    auth_headers = request.META['HTTP_AUTHORIZATION']
    encoded_data = auth_headers.split(' ')[1]
    decoded_data = base64.b64decode(encoded_data).decode('utf-8').split(":") 
    # ['username','password']
    user_name = decoded_data[0]
    password = decoded_data[1]
    if user_name and password:
        user = User.objects.filter(username=user_name)
        if user.exists():
            user = user.first()
            db_password = user.password
            is_match_password = check_password(password, db_password)
            if not is_match_password:
                error_list.append("Invalid Username and Password!")
            else:
                print(user_name)
        else:
            error_list.append("No such user in Database!")
    else:
        error_list.append("Username Password Can Not be Blank!")
    return error_list, user_name, password

class LoginApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        error_list, user_name, password1 = login_data(request)
        if error_list:
            msg = {
                "errors": error_list
            }
            return JsonResponse(msg, status = 404)
        user = authenticate(request, username =user_name, password=password1)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            msg = {
                "username":user.username,
                "eamil":user.email,
                "token": token.key
            }
            return JsonResponse(msg, status =200)
        
class UserRegisterApiView(APIView):
    permission_classes =[]
    authentication_classes = []
    def post(self, request):
        try:
            data = request.data
            error_list = []
            username = str(data['username']).strip() if 'username' in data else ''
            if not username:
                error_list.append("Username can not be balnk!")
            else:
                if User.objects.filter(username=username).exists():
                    error_list.append("Username already exist!")
            password = str(data['password']).strip() if 'password' in data else ''
            if not password:
                error_list.append("Password can not be blank!")

            first_name = str(data['firstName']).strip() if 'firstName' in data else ''
            if not first_name:
                error_list.append("First Name can not be blank!")

            last_name = str(data['lastName']).strip() if 'lastName' in data else ''
            if not last_name:
                error_list.append("Last Name can not be blank!")

            email = str(data['email']).strip() if 'email' in data else ''
            if not email:
                error_list.append("Email can not be blank!")
            else:
                if User.objects.filter(email=email).exists():
                    error_list.append("Email already exist!")

            if error_list:
                msg = {
                    global_code.RESPONSE_CODE_KEY: global_code.UNSUCCESS_RESPONSE_CODE,
                    global_code.RESPONSE_MSG_KEY: "Invalid Data!",
                    global_code.ERROR_KEY: error_list
                }
                return JsonResponse(msg, status = status.HTTP_404_NOT_FOUND)
            with transaction.atomic():
                try:
                    sid = transaction.savepoint()
                    user = User.objects.create_user(username=username,
                                                    first_name=first_name,
                                                    last_name=last_name,
                                                    email=email)
                    user.set_password(password)
                    user.save()
                    UserBalance.objects.create(balance=600, user=user)
                    transaction.savepoint_commit(sid)
                    msg = {
                            global_code.RESPONSE_CODE_KEY: global_code.SUCCESS_RESPONSE_CODE,
                            global_code.RESPONSE_MSG_KEY: "User Register Successfully.",
                    }
                    return JsonResponse(msg, status = status.HTTP_200_OK)
                except Exception as e:
                    transaction.savepoint_rollback(sid)
                    msg = {
                            global_code.RESPONSE_CODE_KEY: global_code.UNSUCCESS_RESPONSE_CODE,
                            global_code.RESPONSE_MSG_KEY: "Internal Server Error!",
                    }
                    return JsonResponse(msg, status = 404)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            msg = {
                    global_code.RESPONSE_CODE_KEY: global_code.UNSUCCESS_RESPONSE_CODE,
                    global_code.RESPONSE_MSG_KEY: "all error!",
            }
            return JsonResponse(msg, status = 500)

        
        