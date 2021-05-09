"""account related url specifing here..."""
# from django.urls import path
from django.conf.urls import url
from .import views
app_name = 'account'

urlpatterns = [
                url(r"^[0-1]*$", views.registration, name="register"),
                url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z_\-]{1,40})$',
                   views.activate, name='activates'),
                url(r'^otpveryfiy$', views.conform_otp, name='verify'),
                url(r'login$', views.login_user, name='login'),
                url(r'^reset_pass$', views.resetpassword, name='resetpassword'),
                url(r'^reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z_\-]{1,40})$',
                   views.set_password, name='rest_password_email'),
                url(r'save$', views.save_new_password, name='saves'),
                url(r"^reset_pass/conform", views.conform_otp_password_reset, name='resetpassword_otp_verify'),
                url(r'logout$', views.logouts, name='logout'),
                url(r'home$', views.home, name='home')
              ]
