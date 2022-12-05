
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from Account.views import (

    about,
    dashboard2,
    home,
    login,
    login2,
    otp,
    register,
    logout,
    profile,
    update_profile,


)

from Recommender.views import (
    homepage,
    dashboard,

)
from Staff.views import (
    addcourse,
    course_delete,
    detail_course_view,
    update_course_view,
)
urlpatterns = [
    path('admin/', admin.site.urls),

    # ACCOUNT

    path('', home, name='home'),
    path('login/', login, name='login'),
    path('login2/', login2, name='login2'),
    path('register/', register, name='register'),
    path('otp/', otp, name='otp'),
    path('logout/', logout, name='logout'),
    path("profile/", profile, name="profile"),
    path("about/", about, name="about"),
    path("profile-update/", update_profile, name="profile-update"),
    path("homepage/", homepage, name="homepage"),
    path("staff-dashboard/", dashboard2, name="dashboard2"),
    path("dashboard/", dashboard, name="dashboard"),
    path("add/", addcourse, name="add"),
    path('detail/<slug>/', detail_course_view, name="detail"),
    path('update/<slug>/', update_course_view, name="update"),
    path('delete/<slug>/', course_delete, name="delete"),


    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="account/password_reset.html"), name='password_reset'),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="account/password_reset_sent.html"), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="account/password_reset_form.html"), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="account/password_reset_complete.html"), name='password_reset_complete'),












]
urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
