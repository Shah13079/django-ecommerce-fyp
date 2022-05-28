
from django.shortcuts import redirect, render
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from accounts.models import Account

from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives

from accounts.forms import Registration,Profile_update

# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Account
from django.urls import reverse,reverse_lazy

#activation email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required



from cart.views import _cart_id
from cart.models import Cart,CartItem

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('my_store:products'))


    if request.method=='POST':
        form=Registration(request.POST)
        context={
            'form':form     }
        if form.is_valid():
            current_site=get_current_site(request)
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            username=form.cleaned_data['username']
            word=form.cleaned_data['password']
            Repeat_password=form.cleaned_data['Repeat_password']
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=word.strip())
            user.save()
            user_id=user.id
            user=Account.objects.get(pk=user_id)

            message=render_to_string(
                f'accounts/account_verification_email.html',{
                    'user':user,
                    'domain':current_site,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user),

                }
            )
            
            to_email=user.email
            mail_subject="ParseJet Account Verification !"
            text_content = ''
            html_content = message
            msg = EmailMultiAlternatives(mail_subject, text_content,email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return redirect('/accounts/login/?command=verification&email='+email)   
    
            # return redirect('login/?command=verification&email='+email)    
    else:
        
        form=Registration()
        context={"form":form}

    return render(request,'accounts/register.html',context)




def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Congratulations! You are ready to go!. ")
        return redirect('accounts:login')
    else:
        messages.error(request,"Inavalid Activation Link ")
        return redirect('register')
    

def view_login(request):
    if request.user.is_authenticated ==True:
        return redirect(reverse_lazy("my_store:products"))

    elif request.method=="POST":
        mail=request.POST.get('email')
        word=request.POST.get('password')
        user=authenticate(request,email=mail,password=word)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    #Getting product variationn  by cart id
                    product_variation = []
                    for item in cart_item :
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    
                    #Get the cart item from user to access him product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list= []
                    id= []
                    for item in cart_item:
                        existing_varitaion = item.variations.all()
                        ex_var_list.append(list(existing_varitaion))
                        id.append(item.id)
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item =  CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user  = user
                            item.save()
                        else:
                            cart_item =  CartItem.objects.get(cart=cart)
                            item.user  = user
                            item.save()




                    
                    # for item in cart_item:
                    #     item.user=user
                    #     item.save()
            except:pass


            login(request,user)
            # messages.SUCCESS(request,"You are now Login.")
            return redirect(reverse_lazy('my_store:store'))
        else:
            messages.error(request,'Invalid Login details !')
            return redirect('accounts:login')
    
    return render(request,'accounts/login.html')


@login_required
def logouting(request):
    logout(request)
    messages.success(request,'You are logged out.')
    return redirect('accounts:login')

#Recovering password sending email
def forgotPassword(request):
    if request.method=="POST":
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email=email)
            #Reset password 
            current_site=get_current_site(request)
            user_id=user.id
           

            message=render_to_string(
            f'accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),

            }
                 )
            
            to_email=user.email
            mail_subject="ParseJet Reset Your Password"

            text_content = ''
            html_content = message
            msg = EmailMultiAlternatives(mail_subject, text_content,email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request,"password Reset email has been send to your email address !")
            return redirect('accounts:login')
        else:
            messages.error(request,"Account does not exists with this email!")
    return render(request,'accounts/forgotpassword.html')



#Validate the ssession and user
def resetpassword_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,"Please Reset your Password")
        return redirect('resetpassword')
    else:
        messages.error(request,"Inavalid Reset Link!")
        return redirect('register')
 


#Update the password
def resetpassword(request):
    if request.method=="POST":
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password==confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password changed succesfully !')
            return redirect('login')

        else:
            messages.error(request,'The Password did not match !')
            return redirect('resetpassword')
    else:
        return render(request,
        'accounts/resetpassword.html')


def ok(request):
    return HttpResponse(request,"ok")


@login_required
def profile_edit(request):
    if request.method=="POST":
      
        form = Profile_update(data=request.POST, instance=request.user)
     
        if form.is_valid():
            # email=form.cleaned_data['Myemail']
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            skills=form.cleaned_data['about_you']
            address=form.cleaned_data['address']

            Account.objects.update(first_name=first_name,last_name=last_name,about_you=skills,address=address)
            
            # messages.success(request,"Profile updated !")
            return render(request,"accounts/profile_edit_data_and_skills.html")
              
    return render(request,"accounts/profile_edit_data_and_skills.html")