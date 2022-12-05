from django.contrib import admin

# Register your models here.
from Account.models import User_Detail, Code


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'username',
        'email',
        'first_name',
        'last_name',
        'phone',
        'county',
        'staff',
        'is_verified'
    )
    # search_fields = (
    #     'user_id',
    #     'username',
    #     'email',
    #     'first_name',
    #     'last_name',
    #     'phone',
    #     'county',

    # )


admin.site.register(User_Detail, UserAdmin)


class CodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code')
    search_fields = ['user']


admin.site.register(Code, CodeAdmin)
