import re
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        email = serializer.validated_data['email']
        if not self.is_valid_email(email):
            raise serializers.ValidationError("Invalid email format")
        serializer.save()

    def is_valid_email(self, email):
        # Email validation pattern using regular expression
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(pattern, email):
            return False
        return True

    def get(self, request):
        return render(request, 'registration.html')

    def post(self, request):
        # Process the registration form submission
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Redirect to the login page
        return redirect('login')

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('filedata-list')
            # return Response({'message': 'Login Successfully'})
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
            # return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        return UserSerializer

    def post(self, request):
        logout(request)
        return redirect('login')
        # return Response('login')

class Instruction(APIView):
    def get(self, request):
        return render(request, 'instruction.html')