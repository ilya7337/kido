# app/registration/views.py
from rest_framework import viewsets, permissions
from registration.models.User.model import User
from registration.models.User.serializers import UserSerializer
from registration.permissions import IsTrainerOrManager

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsTrainerOrManager] 
    