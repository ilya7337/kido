from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'city')
    list_filter = ('role', 'city')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('role', 'phone', 'birth_date', 'city', 
                                                 'parent_name', 'parent_phone', 'rank', 'rank_date')}),
    )