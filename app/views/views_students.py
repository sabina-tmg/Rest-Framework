from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from app.models import Student
from app.serializer import StudentSerializers
from app import global_code
import logging

# Initialize logger
logger = logging.getLogger('django')

class StudentCreateApi(APIView):
    authentication_classes = []
    permission_classes = []
    """This class creates a new student only."""
    
    def post(self, request):
        if not request.body:
            msg = {
                global_code.RESPONSE_CODE_KEY: global_code.UNSUCCESS_RESPONSE_CODE,
                global_code.RESPONSE_MSG_KEY: "Invalid Request Body!"
            }
            return JsonResponse(msg, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer = StudentSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                msg = {
                    global_code.RESPONSE_CODE_KEY: global_code.SUCCESS_RESPONSE_CODE,
                    global_code.RESPONSE_MSG_KEY: "Data created successfully."
                }
                return JsonResponse(msg, status=status.HTTP_201_CREATED)
            
            msg = {
                global_code.RESPONSE_CODE_KEY: global_code.UNSUCCESS_RESPONSE_CODE,
                global_code.RESPONSE_MSG_KEY: "Invalid Data",
                global_code.ERROR_KEY: serializer.errors
            }
            return JsonResponse(msg, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            msg = {
                global_code.RESPONSE_CODE_KEY: global_code.UNSUCCESS_RESPONSE_CODE,
                global_code.RESPONSE_MSG_KEY: "An error occurred."
            }
            return JsonResponse(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Placeholders for other APIs
class StudentListApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            student = Student.objects.filter(is_delete=False)
            #students modal instance 
            serializers = StudentSerializers(student, many=True)# model instance to python
           
            msg = {
                global_code.RESPONSE_CODE_KEY: global_code.SUCCESS_RESPONSE_CODE,
                global_code.RESPONSE_MSG_KEY: "Success",
                "data":serializers.data
            }
            return JsonResponse(msg, status= status.HTTP_200_OK)
            
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            msg = {
                    global_code.RESPONSE_CODE_KEY: global_code.UNSUCCESS_RESPONSE_CODE,
                    global_code.RESPONSE_MSG_KEY: "Invaid Data"
                }
            return JsonResponse(msg, status= status.HTTP_400_BAD_REQUEST)
        

class StudentEditApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request,pk):
        if not request.body:
            msg = {
                global_code.RESPONSE_CODE_KEY: global_code.UNSUCCESS_RESPONSE_CODE,
                global_code.RESPONSE_MSG_KEY: "Invalid Request Body!"
            }
            return JsonResponse(msg, status=status.HTTP_400_BAD_REQUEST)
        try:
            student=Student.object.get(id=pk,is_delter=False)
            serializer = StudentSerializers(student,data=request.data)
            if serializer.is_valid():
                serializer.save()
                msg = {
                    global_code.RESPONSE_CODE_KEY: global_code.SUCCESS_RESPONSE_CODE,
                    global_code.RESPONSE_MSG_KEY: "Data update successfully."
                }
                return JsonResponse(msg, status=status.HTTP_201_CREATED)
            
            msg = {
                global_code.RESPONSE_CODE_KEY: global_code.UNSUCCESS_RESPONSE_CODE,
                global_code.RESPONSE_MSG_KEY: "Invalid Data",
                global_code.ERROR_KEY: serializer.errors
            }
            return JsonResponse(msg, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            msg = {
                global_code.RESPONSE_CODE_KEY: global_code.UNSUCCESS_RESPONSE_CODE,
                global_code.RESPONSE_MSG_KEY: "An error occurred."
            }
            return JsonResponse(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class StudentDeleteApiView(APIView):
    def delete(self, request, id):
        try:
            print(id)
            stundet = Student.objects.get(id=id)
            stundet.is_delete = True
            stundet.save()
            msg = {
                global_code.RESPONSE_CODE_KEY: global_code.SUCCESS_RESPONSE_CODE,
                global_code.RESPONSE_MSG_KEY: "delete Successfully.",
            }
            return JsonResponse(msg, status= status.HTTP_200_OK)
        
        except ObjectDoesNotExist as exe:
            logger.error(str(exe), exc_info=True)
            msg = {
                   global_code.RESPONSE_CODE_KEY:global_code.UNSUCCESS_RESPONSE_CODE,
                   global_code.RESPONSE_MSG_KEY: "No Data Found!"
                }
            return JsonResponse(msg, status= status.HTTP_400_BAD_REQUEST)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            msg = {
                   global_code.RESPONSE_CODE_KEY:global_code.UNSUCCESS_RESPONSE_CODE,
                   global_code.RESPONSE_MSG_KEY: "Invaid Data"
                }
            return JsonResponse(msg, status= status.HTTP_400_BAD_REQUEST)

