from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PatientSerializer,TestSerialiser
from .models import Patient
from rest_framework import status
from django.db.models import Min, Max, Avg , Count , Q
import csv
from io import StringIO


# Create your views here.
class PatientView(APIView):


    def post(self,request,format=None):
        serialiser = PatientSerializer(data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            return Response(serialiser.data,status=status.HTTP_201_CREATED)
        return Response(serialiser.errors,status=status.HTTP_400_BAD_REQUEST)    
    
    def  get(self,request,format=None):
        pid = request.query_params.get('patient_id')
        if(pid is None):
            return Response({"message":"No Patient Id was passed in the query parameters"},status=status.HTTP_400_BAD_REQUEST)
        tests = Patient.objects.filter(patient_id = pid)
        serialiser = TestSerialiser(tests, many = True)
        return Response(serialiser.data,status=status.HTTP_200_OK)

class TestStatisticsView(APIView):

    def get(self,request,format=None):
        test_statistics = (
            Patient.objects.values('test_name')
            .annotate(
                min_value=Min('value'),
                max_value=Max('value'),
                avg_value=Avg('value'),
                total_tests= Count('id'),
                abnormal_count = Count('id',filter=Q(is_abnormal=True))
            )
        )
        test_data = {
             "test_stats": {
                stat['test_name']: {
                    "min_value": float(stat['min_value']),
                    "max_value": float(stat['max_value']),
                    "avg_value": float(stat['avg_value']),
                    "total_tests": stat['total_tests'],
                    "abnormal_count": stat['abnormal_count']
                }
                for stat in test_statistics
             }
        }
        return Response(test_data,status=status.HTTP_200_OK)

class UploadCSVView(APIView):
    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
          
            decoded_file = csv_file.read().decode('utf-8')
            csv_reader = csv.DictReader(StringIO(decoded_file))
            
           
            patients = []
            errors = []

            for row_number, row in enumerate(csv_reader, start=1):
                serializer = PatientSerializer(data=row)
                if serializer.is_valid():
                    patients.append(Patient(**serializer.validated_data))
                else:
                    errors.append({f"Row {row_number}": serializer.errors})
            
            
            if patients:
                Patient.objects.bulk_create(patients)
            
            response = {
                "success": f"{len(patients)} records added successfully",
                "errors": errors,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
