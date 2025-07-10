from rest_framework import serializers
from registration.models.StudentEnrollmentRequest.model import StudentEnrollmentRequest


class StudentEnrollmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEnrollmentRequest
        fields = ['id', 'trainer', 'student', 'status', 'created_at', 'updated_at']
        read_only_fields = ['trainer', 'status', 'created_at', 'updated_at']

    def validate(self, data):
        if self.context['request'].user.role != 'trainer':
            raise serializers.ValidationError("Only trainers can create enrollment requests")
        return data
