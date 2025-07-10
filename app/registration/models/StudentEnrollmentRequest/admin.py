from django.contrib import admin

class StudentEnrollmentRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'trainer', 'student', 'status', 'created_at')
    list_filter = ('status', 'trainer')
    search_fields = ('trainer__username', 'student__username')
    list_editable = ('status',)
    raw_id_fields = ('trainer', 'student')
    date_hierarchy = 'created_at'