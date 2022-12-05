from django.contrib import admin
from .models import Course, Deleted_Course, Rating, Updated_Course

# Register your models here.


class courseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'faculty',
        'tution_fees',
        'image',
        'intake_in',
        'academic_year',
        'entry_year',
        'lectures',
        'location',
        'schools',
        'school_phone',
        'school_email',
    )
    search_fields = (
        'id',
        'title',
        'schools',
        'location',
        'intake_in',
        'school_phone',
        'school_email',
        
    )


class ratingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'course',
        'rating',
        'rated_date',
    )


class deletedAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone',
        'course_id',
        'date',
    )
    search_fields = (
        'user',
    )


class updatedAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone',
        'course_id',
        'date',
    )
    search_fields = (
        'user',
    )


admin.site.register(Course, courseAdmin)
admin.site.register(Rating, ratingAdmin)
admin.site.register(Deleted_Course, deletedAdmin)
admin.site.register(Updated_Course, updatedAdmin)
