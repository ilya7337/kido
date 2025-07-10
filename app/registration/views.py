from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from registration.models.JWT.serializers import CustomTokenObtainPairSerializer
from registration.models.User.serializers import UserSerializer
from registration.models.StudentEnrollmentRequest.serializers import StudentEnrollmentRequestSerializer
from .models import User as CustomUser, StudentEnrollmentRequest
from rest_framework_simplejwt.tokens import RefreshToken
from registration.permissions import IsTrainerManagerOrAdmin

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.get('refresh')
        # Удаляем refresh из тела ответа
        if 'refresh' in response.data:
            del response.data['refresh']
        # Кладём refresh в httpOnly cookie
        response.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            secure=True, 
            samesite='Lax', 
            max_age=60*60*24*7  
            )
        return response

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsTrainerManagerOrAdmin]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        StudentEnrollmentRequest.objects.create(
            trainer=request.user,  # кто регистрирует
            student=user,          # кого регистрируют
            status=StudentEnrollmentRequest.PENDING
        )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
class LogoutView(generics.GenericAPIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            response = Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_200_OK
            )
            response.delete_cookie('refresh_token')
            return response
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class StudentEnrollmentRequestView(generics.CreateAPIView):
    queryset = StudentEnrollmentRequest.objects.all()
    serializer_class = StudentEnrollmentRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # ПРоверяем текущего пользователя на роль тренера
        if self.request.user.role != 'trainer':
            raise Exception("Only trainers can create enrollment requests")
        serializer.save(trainer=self.request.user)
    