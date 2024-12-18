from django.urls import path
from .views import PatientView,TestStatisticsView,UploadCSVView

urlpatterns = [
    path('tests/', PatientView.as_view(),name='test_create_retrieve'),
    path('tests/stats/',TestStatisticsView.as_view(),name='test_stats'),
    path('upload-csv/', UploadCSVView.as_view(), name='upload_csv')
]
