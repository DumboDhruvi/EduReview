from django.urls import path
from .views import home, signup, user_login, logout_view, course_detail, search

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('search/', search, name='search'),
    path('<str:course_name>/', course_detail, name='course_detail'),
]
