"""defining views here .."""
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template import loader
import requests

from .models import User

from .token import account_activation_token
from .forms import Registration, OTP, Login, PasswordReset, PasswordSet


# Create your views here


def registration(request):
    """User registration .."""
    form = Registration()
    if request.method == "POST":
        form = Registration(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            email_or_phone = form.cleaned_data.get('username')

            if '@' in email_or_phone:
                current_site = get_current_site(request)
                mail_subject = "Activate your codeacess account"

                message = render_to_string('account/activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user), })

                message.content_subtype = 'html'
                message = strip_tags(message)
                to_email = form.cleaned_data.get('username')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return HttpResponse('Please cheack your email to complete the registration')
            else:
                # https://2factor.in/API/V1/{api_key}/SMS/+91{user's_phone_no}/AUTOGEN
                # { "Status": "Success", "Details": "5D6EBEE6-EC04-4776-846D"}
                    api_key = 'c1003ac3-a97d-11e9-ade6-0200cd936042'
                    # api_key = '20528aa7-ccfa-11ea-9fa5-0200cd936042'
                # try:
                    phone_no = '+91' + email_or_phone
                    message = None
                    print(phone_no)
                    status = requests.post("https://2factor.in/API/V1/" + api_key + "/SMS/" + phone_no + "/AUTOGEN", data={}).json()
                    # status = status.json()
                    # print(type(status),status)
                    request.session['session_id'] = status.get("Details")
                    # print(request.session)
                    if status.get('Status') == "Success":
                        # print(status)
                        # message = "enter otp"
                        request.user = email_or_phone
                        request.session['pk'] = user.pk
                        form = OTP()

                        return render(request, 'account/otp_verifiction.html', {'form': form})

    return render(request, 'account/registration.html', {"form": form, 'title': 'Registration', 'first_buton': 'Register', "second_button": "Login"})


def activate(request, uidb64, token):
    """Activating account.."""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #   login(request, user)
        #   return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        user.delete()

        return HttpResponse('Activation link is invalid!')


def conform_otp(request):
    """Verfiying OTP .."""
    if request.method == 'POST':
        # https://2factor.in/API/V1/{api_key}/SMS/VERIFY/{session_id}/{otp_entered_by_user}
        api_key = 'c1003ac3-a97d-11e9-ade6-0200cd936042'
        form = OTP(request.POST)
        user = User.objects.get(pk=request.session.get('pk'))
        if form.is_valid():

            otp = form.cleaned_data.get('otp_input')
            verify = "https://2factor.in/API/V1/" + api_key + "/SMS/VERIFY/" + request.session.get('session_id') + "/" + otp
            status = requests.post(verify).json()
            # status = status.json()
            # user = User.objects.get(pk=request.session.get('pk'))
            print(status)
            if user and status.get('Status') == 'Success':
                user.is_active = True
                user.save()
                # new_group, created = Group.objects.get_or_create(name ='staff')
                # user.groups.add(new_group)
                # login(request, user)p
            # return redirect('home')
            return HttpResponse('Thank you for your mobile no is verified. Now you can login your account.')
        else:
            user.delete()
            return HttpResponse('Activation link is invalid!')


def login_user(request):
    """Login view .."""
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('user_name')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                try:
                    login(request, user)
                    return redirect('account:home')
                except:
                    pass
    form = Login()

    return render(request, 'account/registration.html', {"form": form, 'title': 'Login', 'first_buton': 'Login', "second_button": "Register"})


def resetpassword(request):
    """Reset user possword ..."""
    if request.method == 'POST':
        form = PasswordReset(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get('username')
            associated_users = User.objects.filter(username=data)
            if associated_users.exists():
                associated_user = associated_users.get()
                if '@' in associated_user.username:
                    current_site = get_current_site(request)
                    mail_subject = "Rest_password codeacess account"
                    template_html = 'account/reset_email_pasword.html'
                    text_content = "Reset Password"
                    email_context = {
                        'user': associated_user.username,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                        'token': account_activation_token.make_token(associated_user), }


                    # message = render_to_string('account/reset_email_pasword.html', {
                    #     'user': associated_user.username,
                    #     'domain': current_site.domain,
                    #     'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    #     'token': account_activation_token.make_token(associated_user), })
                    html = loader.get_template(template_html)
                    html_content = html.render(email_context)

                    # message.content_subtype = 'html'
                    # message = strip_tags(message)
                    to_email = form.cleaned_data.get('username')
                    email = EmailMultiAlternatives(mail_subject, text_content, to=[to_email])
                    email.attach_alternative(html_content, "text/html")
                    email.send()
                    return HttpResponse('Please cheack your email to resetpassword')
                else:
                    # https://2factor.in/API/V1/{api_key}/SMS/+91{user's_phone_no}/AUTOGEN
                    # { "Status": "Success", "Details": "5D6EBEE6-EC04-4776-846D"}
                        api_key = 'c1003ac3-a97d-11e9-ade6-0200cd936042'
                        # api_key = '20528aa7-ccfa-11ea-9fa5-0200cd936042'
                    # try:
                        phone_no = '+91' + associated_user.username
                        message = None
                        print(phone_no)
                        status = requests.post("https://2factor.in/API/V1/" + api_key + "/SMS/" + phone_no + "/AUTOGEN", data={}).json()
                        # status = status.json()
                        # print(type(status),status)
                        request.session['session_id'] = status.get("Details")
                        # print(request.session)
                        if status.get('Status') == "Success":
                            # print(status)
                            # message = "enter otp"
                            request.user = associated_user.username
                            request.session['pk'] = associated_user.pk
                            form = OTP()

                            return render(request, 'account/change_password_otp.html', {'form': form})
    form = PasswordReset()
    return render(request, 'account/reset_pass.html', {'form': form})


def set_password(request, uidb64, token):
    """Validate reset passs .."""
    if request.method != "POST":
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            request.session['pk'] = uid
            form = PasswordSet()
            return render(request, 'account/new_password.html', {'form': form})


def conform_otp_password_reset(request):
    """Verfiying OTP .."""
    if request.method == 'POST':
        # https://2factor.in/API/V1/{api_key}/SMS/VERIFY/{session_id}/{otp_entered_by_user}
        api_key = 'c1003ac3-a97d-11e9-ade6-0200cd936042'
        form = OTP(request.POST)
        user = User.objects.get(pk=request.session.get('pk'))
        if form.is_valid():

            otp = form.cleaned_data.get('otp_input')
            verify = "https://2factor.in/API/V1/" + api_key + "/SMS/VERIFY/" + request.session.get('session_id') + "/" + otp
            status = requests.post(verify).json()
            # status = status.json()
            # user = User.objects.get(pk=request.session.get('pk'))

            if user and status.get('Status') == 'Success':
                form = PasswordSet()
                return render(request, 'account/new_password.html', {'form': form})

            return HttpResponse('invalid otp.')


def save_new_password(request):
    """Set new password.."""
    if request.method == "POST":
        form = PasswordSet(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.session['pk'])
            user.set_password(form.clean_password2())
            user.save()
            return HttpResponse("password updated")


@login_required
def logouts(request):
    """Log out view.."""
    logout(request)
    return redirect('account:login')


@login_required
def home(request):
    """Home page Rendering .."""
    return render(request, 'account/home.html', {'title': 'home'})
