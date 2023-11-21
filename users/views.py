from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from actions.models import Action


# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        role = request.POST.get('roleRadio')
        user = User.objects.create_user(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.details.role = role
        user.save()
        request.session['username'] = user.username
        request.session['role'] = user.details.role
        messages.add_message(request, messages.SUCCESS, "You created an account for: %s" % user.username)
        return redirect('myEventsApp:events_list')
    else:
        return render(request, 'users/user/register.html')


def profile(request, username):
    user = get_object_or_404(User, username=username)
    actions = Action.objects.filter(user_id=user.id)
    if request.method == "POST":
        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        new_password = request.POST.get('new_password')
        if new_password:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password has been updated.')
        user.email = request.POST.get('email')
        user.details.role = request.POST.get('roleRadio')
        user.save()
        messages.add_message(request, messages.INFO, "You successfully edited the user: %s" % user.username)
        return redirect('users:profile', user.username)
    return render(request, 'users/user/profile.html', {"user": user, "actions": actions})


def admin_panel(request):
    users = User.objects.all()
    if request.method == "POST":
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        user.details.role = request.POST.get('roleRadio')
        user.save()
        return redirect('users:admin_view')
    return render(request, 'users/user/admin-panel.html', {"users": users})

def login_user(request):
    username = request.POST.get("username")
    pw = request.POST.get("pw")

    user = authenticate(username=username, password=pw)

    if user is not None:
        request.session['username'] = user.username
        request.session['role'] = user.details.role
        messages.add_message(request, messages.SUCCESS, "Logged in successfully")
    else:
        messages.add_message(request, messages.WARNING, "Invalid username or password")

    return redirect("myEventsApp:events_list")


def logout_user(request):
    del request.session['username']
    del request.session['role']
    return redirect("myEventsApp:home")
