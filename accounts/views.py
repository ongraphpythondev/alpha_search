from django.shortcuts import render, redirect
from accounts.models import User, JwtToken
import jwt
from main.settings import *
import datetime
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import auth

# Create your views here.
def generate_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=int(env("JWTDAYS"))),
        'iat': datetime.datetime.utcnow(),
        'sub': str(user_id)
    }
    return jwt.encode(payload, env("SECRET_KEY"), algorithm=env("ALGORITHM"))

def verify_token(token):
    try:
        token_obj = JwtToken.objects.filter(access_token= token, is_block__in = [False])
        if not token_obj:
            return False
        payload = jwt.decode(token, env("SECRET_KEY"), algorithms=[env("ALGORITHM")])
        user_id = payload['sub']
        return User.objects.filter(id = user_id).first()
    except:
        return False

@method_decorator(csrf_exempt, name='dispatch')
class Signup(View):

    def get(self, request):
        user = verify_token(request.COOKIES.get('access_token'))
        if user:
            return redirect("accounts:profile_user")
        return render(request, "accounts/signup.html")

    def post(self, request):
        data = request.POST
        if not ((data.get("email") or data.get("email") != "") and (data.get("password") or data.get("password") != "") and\
            (data.get("first_name") or data.get("first_name") != "") and (data.get("last_name") or data.get("last_name") != "") and\
            (data.get("company") or data.get("company") != "") ):
            return render(request, "accounts/signup.html",{"errors": "Must required email, password, first_name, last_name, company"})
        if User.objects.filter(email = data.get("email")):
            return render(request, "accounts/signup.html",{"errors": "Email is already present"})
        user = User.objects.create(email= data["email"], password= data["password"],\
                    first_name= data["first_name"], last_name= data["last_name"],\
                    company= data["company"], is_active= True)
        token = generate_token(user.id)
        JwtToken.objects.create(user= user, access_token= token, is_block= False)
        response = redirect("accounts:profile_user")
        response.set_cookie('access_token', token)  
        return response

@method_decorator(csrf_exempt, name='dispatch')
class Login(View):

    def get(self, request):
        user = verify_token(request.COOKIES.get('access_token'))
        if user:
            return redirect("accounts:profile_user")
        return render(request, "accounts/login.html")

    def post(self, request):
        data = request.POST
        if not ((data.get("email") or data.get("email") != "") and (data.get("password") or data.get("password") != "")):
            return render(request, "accounts/login.html",{"errors": "Must required email and password"})
        user = auth.authenticate(email= data["email"], password= data["password"])
        if user:
            token = generate_token(user.id)
            JwtToken.objects.create(user= user, access_token= token, is_block= False)
            response = redirect("accounts:profile_user")
            response.set_cookie('access_token', token)  
            return response
        return render(request, "accounts/login.html", {"errors": "User not found"})

@method_decorator(csrf_exempt, name='dispatch')
class Logout(View):

    def get(self, request):
        user = verify_token(request.COOKIES.get('access_token'))
        if user:
            JwtToken.objects.filter(access_token = request.COOKIES.get('access_token')).update(is_block= True)
            response = redirect("accounts:login_user")
            response.delete_cookie('access_token')
            return response
        return redirect("accounts:login_user")

@method_decorator(csrf_exempt, name='dispatch')
class Profile(View):

    def get(self, request):
        user = verify_token(request.COOKIES.get('access_token'))
        if user:
            return render(request, "accounts/profile.html", {"username": user.first_name})
        return redirect("accounts:login_user")


