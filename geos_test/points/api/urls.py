from django.urls import path
from .views import PointPageView, AllPointRecordsView, SendPointRecordsView

urlpatterns = [
    path('api/', AllPointRecordsView.as_view()), #returns all records
    path('api/<int:from_point>', PointPageView.as_view()), #returns certain record by obj_id
    path('api/<str:method>/from/<int:from_point>/to/<int:to_point>', SendPointRecordsView.as_view())
]
