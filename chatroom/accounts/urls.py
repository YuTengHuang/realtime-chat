from django.urls import path
from .serializers import LoginSerializer
from .views import SignupView, GetAllAccountView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginSerializer.as_view(), name='login'),
    path('allAccount/', GetAllAccountView.as_view(), name='getAllAccount'),
]
