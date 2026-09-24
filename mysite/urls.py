from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from home.forms import LoginForm, CustomPasswordResetForm, CustomSetPasswordForm



urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('home.urls')),

    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Password Reset Routes
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        form_class=CustomPasswordResetForm,
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        form_class=CustomSetPasswordForm
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
