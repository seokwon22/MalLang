from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
# from django.contrib.auth.hashers import make_password, check_password
from user.models import Board, Member, Diary


def login(request):
    if request.method == "GET":
        return render(request, "user/login.html")
    else:
        user_id = request.POST["user_id"]
        password = request.POST["password"]

    try:
        member = Member.objects.get(user_id=user_id)
        member_password = member.password

        if password == member_password :
            request.session["nickname"] = member.nickname
            request.session["user_id"] = member.user_id
            return render(request, "MalLang/main.html")

        else:
            return render(request, 'user/login.html', {'error':'아이디 혹은 비밀번호가 일치하지 않습니다.'})
    except Member.DoesNotExist:
            return render(request, 'user/login.html', {'error': '존재하지 않는 아이디입니다.'})


def logout(request):
    del request.session["user_id"]
    return redirect("user:login")

def register(request):
    if request.method == "GET":
        return render(request, 'user/register.html')
    else:
        user_id = request.POST["user_id"]
        nickname = request.POST["nickname"]
        password = request.POST["password"]
        # print(len(make_password(password)))

        insert_member = Member.objects.create(nickname=nickname, user_id=user_id, password=password)

        if insert_member:
            return redirect("user:login")
        else:
            return redirect("user:register")

        # DB에서 PASSWORD 컬럼 사이즈 확인


