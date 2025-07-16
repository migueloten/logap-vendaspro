from django.urls import path
from .jwt_views import (
    CustomTokenObtainPairView,
    logout_view,
    user_profile,
    verify_token
)

urlpatterns = [
    # Endpoints JWT principais
    path('login/', CustomTokenObtainPairView.as_view(), name='auth-login'),
    path('logout/', logout_view, name='auth-logout'),
    path('profile/', user_profile, name='auth-profile'),
    path('verify/', verify_token, name='auth-verify'),
]
