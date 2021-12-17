from django.urls import path
from prediction.api import views

app_name = 'prediction'

urlpatterns = (
    path(
        'predict/',
        views.PredictView.as_view(),
        name='predict'
    ),
)
