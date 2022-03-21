from django.shortcuts import render,redirect
from .models import Registration,Course
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from . tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse

def dashboard(request,user):
    coursedata=Course.objects.all().values()
    return render(request,"matg/dashboard.html",{"card":coursedata,"user":user})

def home(request):
    sename=request.session.get("sename","")
    sepassword=request.session.get("sepassword","")
    print(sename,sepassword)
    if(request.method=="POST") and "signin" in request.POST:
        username=request.POST.get("loginName")
        userpassword=request.POST.get("loginPassword")
        try:
            user=Registration.objects.get(email=username)
            if(user.password==userpassword and  user.is_active==True):
                request.session["sename"]=username
                request.session["sepassword"]=userpassword
                return redirect("dashboard/"+str(username))
            else:
                message="Password wrong"
                return render(request,"matg/home.html",{"loginmsg":message})
        except:
            message="User Does't Exists"
            return render(request,"matg/home.html",{"loginmsg":message})
    if(request.method=="POST") and "signup" in request.POST:
        uname=request.POST.get("signupname")
        uemail=request.POST.get("signupemail")
        umobile=request.POST.get("signupphone")
        upassword=request.POST.get("signuppassword")
        try:
            user=Registration.objects.create(name=uname,phone=umobile,email=uemail,password=upassword,is_active=False)
        except:
            message="User Alredy Exists"
            return render(request,"matg/home.html",{"message":message})
        uidb64=urlsafe_base64_encode(force_bytes(user.pk))
        currentsite=get_current_site(request).domain
        link=reverse('activate',kwargs={'uidb64':uidb64,'token':account_activation_token.make_token(user)})
        activate_url="http://"+currentsite+link
        message="hi "+uname+"click below link to verify\n"+activate_url
        email=EmailMessage("Account Activation",message,to=[uemail])
        email.send()
        message="Activation Link sent to E-mail"
        return render(request,"matg/home.html",{"message":message})
    return render(request,"matg/home.html",{"email":sename,"password":sepassword})
    
def activate(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=Registration.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,user.DoesNotExist):
        user=None
    if(user is not None and account_activation_token.check_token(user,token)):
       user.is_active=True
       user.save()
       return render(request,"matg/success.html")
    else:
        return HttpResponse("failed verification")
