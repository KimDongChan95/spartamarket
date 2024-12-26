from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Profile

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 회원가입 후 자동 로그인
            return redirect('home')  # 회원가입 후 리다이렉트
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')

def profile(request, username):
    user = get_object_or_404(User, username=username)
    products = user.products.all()  # related_name='products' 사용
    liked_products = user.liked_products.all()  # 찜한 물건
    return render(request, 'profile.html', {
        'user': user,
        'products': products,
        'liked_products': liked_products,
    })

def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    # Profile 객체가 없을 경우 생성
    if not hasattr(user_to_follow, 'profile'):
        Profile.objects.create(user=user_to_follow)

    profile = user_to_follow.profile

    if request.user in profile.followers.all():
        profile.followers.remove(request.user)  # 이미 팔로우한 경우 언팔로우
    else:
        profile.followers.add(request.user)  # 팔로우 추가

    return redirect('profile', username=username)  # 프로필 페이지로 리다이렉트