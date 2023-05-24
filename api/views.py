from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .permissions import ObjectOwner
from .serializer import UserSerializer, SelfSerializer, SignupSerializer


class HomeView(APIView):
    def get(self, request):
        return Response({"message": "App Initialized"}, status=status.HTTP_200_OK)


class SignupView(APIView):
    serializer_class = SignupSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"message": "You are not authenticated"})
        user = request.user.username
        return Response({"message": f"You are authenticated as {user}, Logout before authenticating again"}, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user.username
            return Response({"message": f"You are authenticated as {user}"}, status=status.HTTP_200_OK)

        data = request.data
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return Response({"message": f"You are authenticated as {user}"}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def get(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        logout(request)
        return Response({"message": "Logged out"}, status=status.HTTP_200_OK)

class UsersView(APIView):
    model = CustomUser
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_superuser:
            users = [user for user in self.model.objects.all() if not user.is_superuser or not user.is_staff]
        else:
            users = self.model.objects.all()

        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_superuser:
            serializer = SignupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)

class UserView(APIView):
    model = CustomUser
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ObjectOwner]

    def get(self, request, pk=None):
        user = self.model.objects.filter(id=pk).first()
        if user:
            serializer = self.serializer_class(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk=None):
        user = self.model.objects.filter(id=pk).first()
        serializer = self.serializer_class(user, data=request.data)
        if user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = self.model.objects.filter(id=pk).first()
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class SelfView(APIView):
    model = CustomUser
    serializer_class = SelfSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.model.objects.filter(id=request.user.id).first()
        if user:
            serializer = self.serializer_class(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = self.model.objects.filter(id=request.user.id).first()
        serializer = self.serializer_class(user, data=request.data)
        if user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


