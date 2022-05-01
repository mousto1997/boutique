from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.views import View

from apps.users.models import Customer
from apps.users.decorators import unauthenticated_user, allowed_users
from apps.users.forms import CreationUserForm
from django.http import JsonResponse
from apps.users.utils import token_generator


# Create your views here.
@unauthenticated_user
def register(request):
    form = CreationUserForm()
    if request.method == 'POST':
        form = CreationUserForm(request.POST)
        email = request.POST['email']
        if not User.objects.filter(email=email).exists():
            if form.is_valid():
                user = User.objects.create_user(username=request.POST['username'], email=email)
                user.set_password(request.POST['password1'])
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                    'uidb64': uidb64, 'token': token_generator.make_token(user), 'username': user.username
                })
                activate_url = 'http://'+domain+link
                email_subject = 'Activate your account'
                email_body = 'Hello ' + user.username+\
                    '. Please use this link to activate your account.\n'+ activate_url

                email = EmailMessage(
                    email_subject, email_body, 'noreply@semycolon.com', [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account was created successfully, Please go to your email to activate your account.')
                return redirect('login')
        else:
            form = CreationUserForm()
            messages.warning(request, 'This email is already used by someone.')
    context = {'form': form}
    return render(request, 'register.html', context)


class verificationView(View):
    def get(self, request, uidb64, token, username):
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        messages.success(request,  f'Your account has been activated. You can login now.')
        return redirect('login')
