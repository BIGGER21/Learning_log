from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout,login,authenticate
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def logout_view(request):
    """LOGOUT"""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))

def register(request):
    """register new account"""
    if request.method != 'POST':
        """display null register form"""
        form = UserCreationForm()
    else:
        """handle the posted form"""
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            """Let the user log in automatically,and redirect to the index"""
            authenticated_user = authenticate(username=new_user.username,password=request.POST['password1'])
            login(request,authenticated_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))

    context = {'form':form}
    return render(request,'users/register.html',context)