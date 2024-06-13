from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from .models import Item
from .forms import ItemForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return redirect(request, 'login')
    else:
     form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('profile')

    def get_success_url(self):
        return self.success_url


def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'home2.html')
    else:
        return render(request, 'home.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')



def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def add_item_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {'form': form})

@login_required
def inventory_view(request):
    items = Item.objects.all()
    return render(request, 'inventory.html', {'items': items})

@login_required
def item_detail_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'item_detail.html', {'item': item})

@login_required
@user_passes_test(is_admin)
def delete_item_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('inventory')
    return render(request, 'delete_item.html', {'item': item})