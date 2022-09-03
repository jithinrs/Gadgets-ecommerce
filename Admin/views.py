from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import logout,login,authenticate
from .form import UserForm,Account
from django.contrib.admin.views.decorators import staff_member_required 
# Create your views here.
def Admin_login(request):
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect(Admin_page) 
        else:
            messages.error(request,'user does not exist..')
            return redirect(Admin_login)
    return render(request,'Admin/login.html')

@staff_member_required(login_url='admin_login')
def Admin_page(request):
    return render(request,'Admin/dashbord.html')


def Admin_logout(request):
    logout(request)
    return redirect(Admin_login)



#To display all user

def user_display(request):
    user=Account.objects.filter(is_superadmin = False)
    form = UserForm()
    context={
        'user':user,
        'form':form
    }
    return render(request,'Admin/admin-display-user.html',context) 

def user_block(request,id,flag):
    if request.method == 'POST':
         if flag ==1:
            user = Account.objects.get( id = id)
            user.is_active = False
            print('user is blocked')
            user.save()
         else: 
            user = Account.objects.get( id = id)
            user.is_active = True
            print('user is blocked')
            user.save()
         return redirect(user_display)