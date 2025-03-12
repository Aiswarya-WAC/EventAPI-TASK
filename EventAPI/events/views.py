from datetime import timedelta
from django.contrib.auth.models import User
from events.serializers import EventSerializer, RegisterSerializer, UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Event
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import send_mail
from django.utils.timezone import now

class RegisterView(APIView):  
    def post(self, request):
        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({"detail": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username:
            return Response({"detail": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({"detail": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class EventListCreateView(APIView):
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        events = Event.objects.filter(owner=request.user)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("user=",request.user)
        user = request.user
        event_date = request.data.get("start_date")[:10]  

        if Event.objects.filter(owner=user, start_date__date=event_date).exists():
            return Response(
                {"error": "You already have an event scheduled on this date."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save(owner=request.user)

            send_mail(
                subject="Event Scheduled Successfully",
                message=f"Dear {user.username},\n\nYour event '{event.title}' is scheduled on {event.start_date}.",
                from_email="dairyhubservices@gmail.com", 
                recipient_list=[user.email],
                fail_silently=False,
            )
            print(f" Email Sent: Event '{event.title}' created for {request.user} at {request.user.email}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EventDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, id):
        
        try:
            event = Event.objects.get(id=id, owner=request.user)
            event.delete()
            return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            return Response({"error": "Event not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)
        

class ListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        end_date = now() + timedelta(days=30)
        events = Event.objects.filter(owner=user, start_date__lte=end_date)
        return Response(EventSerializer(events, many=True).data)

