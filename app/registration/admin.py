from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentEnrollmentRequest
from registration.models.User.admin import CustomUserAdmin
from registration.models.StudentEnrollmentRequest.admin import StudentEnrollmentRequestAdmin


admin.site.register(User, CustomUserAdmin)
admin.site.register(StudentEnrollmentRequest, StudentEnrollmentRequestAdmin)
