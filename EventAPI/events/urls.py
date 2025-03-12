
from django.urls import path
from .views import  EventDeleteView, RegisterView, LoginView , EventListCreateView ,ListAPIView
urlpatterns = [
  
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('events/', EventListCreateView.as_view(), name='event-list'),
    path('delete/<int:id>/', EventDeleteView.as_view(), name='event-delete'),
    path('lists/',ListAPIView.as_view() , name="list"),
 
]