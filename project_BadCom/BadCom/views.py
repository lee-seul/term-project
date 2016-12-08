# coding: utf-8

from wiki.forms import SignupForm
from django.shortcuts import redirect, render
from django.contrib.auth import login as django_login
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import is_safe_url
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

def signup(request):
    var = {}
    if request.method == "POST":
        form = SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = SignupForm()
        var['form'] = form

    return render(request, 'signup.html', var)

class LoginView(FormView):
    success_url = '/'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'login.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        django_login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to

