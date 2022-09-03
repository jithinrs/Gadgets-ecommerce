from django.shortcuts import render,redirect
from .models import Account
from.form import RegistrtationForm
from django.contrib import messages,auth
from .verify import send_otp, verify_otp
from .form import *
from .models import *
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def Register(request):
    if request.method=='POST':
        form=RegistrtationForm(request.POST)
        if form.is_valid:
            first_name = request.POST['first_name']
            last_name  = request.POST['last_name']
            email      = request.POST['email']
            mobile     = request.POST['mobile']
            password   = request.POST['password']

            request.session['first_name'] = first_name
            request.session['last_name']  = last_name
            request.session['email']      = email
            request.session['mobile']     = mobile
            request.session['password']   = password
            
            print("mobile: ",mobile)
            send_otp(mobile)
            return redirect('verify')
    form=RegistrtationForm()
    context ={'form':form}
    return render(request,'Accounts/register.html',context)

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Account.objects.get(email=email)
        except :
            messages.error(request,"user Does not exist..")
        user = authenticate(request,email=email,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home') 
        else:
            messages.error(request,'user does not exist..')
            return redirect('login')
    return render(request,'Accounts/login.html')
def Logout(request):
    logout(request)
    return redirect('home')



def verify_code(request):
    if  request.method == 'POST':
        otp_check = request.POST.get('otp')
        mobile=request.session['mobile']

        verify=verify_otp(mobile,otp_check)

        if  verify:
            messages.success(request,'account has created successfuly please login now') 

            first_name = request.session['first_name']
            last_name  = request.session['last_name']
            email      = request.session['email']
            mobile     = request.session['mobile']
            password   = request.session['password']

            user = Account.objects.create_user(
                first_name =  first_name,
                last_name  =  last_name,
                email      =  email,
                mobile     =  mobile,
                password   =  password
            )
            user.is_verified = True
            user.save()
            messages.success(request,'Registration Successful')
            return redirect('login')
        
        else:
            messages.error(request,'invalid otp recheck')
            return redirect ('verify_code')
        
    return render(request,'Accounts/verify.html')


