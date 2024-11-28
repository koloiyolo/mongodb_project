from django.shortcuts import render, redirect
from .forms import SignUpForm, FilmForm, UserDataForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.timezone import now

from .models import Film, Rental, UserData

# Create your views here.


def home(request):
    rentals = None
    films = Film.objects.all()
    for film in films:
        if Rental.objects.filter(film=film, return_date__isnull=True).exists():
            film.stock = False
        else:
            film.stock = True
            
    if request.user.is_authenticated:
        rentals = Rental.objects.filter(user=request.user, return_date__isnull=True)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.success(request, "Nieudana próba logowania, spróbuj ponownie!")
            return redirect('home')

    else:
        return render(request, 'users/home.html', { 'films':films, 'rentals':rentals})
    return redirect('home')

def user_logout(request):
    logout(request)
    messages.success(request, "Wylogowano użytkownika")
    return redirect('home')

def user_register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            UserData.objects.create(user=user)
            login(request, user)
            messages.success(request, "Utworzono nowe konto!")
            return redirect('home')
        pass
    else:
        form = SignUpForm()
        return render(request, 'users/register.html', {'form': form})
        
    return render(request, 'users/register.html', {'form': form})

def user_list(request):
    if request.user.is_authenticated:
        users = User.objects.all()
        q = request.GET.get('search', '')
        if q is not None:
            users = User.objects.filter(
                username__icontains=q
                ) | User.objects.filter(
                first_name__icontains=q
                ) | User.objects.filter(
                last_name__icontains=q
                )

        for user in users:
            user.userdata = UserData.objects.get(user=user)

        return render(request, 'users/list.html', { 'users':users})
    else:
        return redirect('home')

def user_edit(request, pk):
    if request.user.is_authenticated:
        userdata = UserData.objects.filter(user=pk).first()
        form = UserDataForm(request.POST or None, instance=userdata)
        if request.method =='POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Użytkownik zaktualizowany")
                return redirect('user_list')
        else:
            return render(request, 'users/form.html', {'form':form})
    else:
        return render(request, 'users/form.html', {'form':form})

def user_remove(request, pk):
    if request.user.is_authenticated:
        delete_it = User.objects.get(id=pk)
        if request.user.id == delete_it.id:
            messages.success(request, "Nie można usunąć siebie")
        elif Rental.objects.filter(user=delete_it, return_date__isnull = True).exists():
            messages.success(request, "Użytkownik ma wypożyczone filmy")
        else: 
            delete_it.delete()
            messages.success(request, "Użytkownik usunięty")
        return redirect('user_list')
    else:
        return redirect('home')

def edit(request):
    if request.user.is_authenticated:
        userdata = UserData.objects.filter(user=request.user).first()
        form = UserDataForm(request.POST or None, instance=userdata)
        if request.method =='POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Użytkownik zaktualizowany")
                return redirect('home')
        else:
            return render(request, 'users/form.html', {'form':form})
    else:
        return render(request, 'users/form.html', {'form':form})
    return redirect('home')

# Films
def film_list(request):
    if request.user.is_authenticated:
        users = None
        if request.user.is_staff:
            users = User.objects.all()

        films = Film.objects.all()
        q = request.GET.get('search', '')
        if q is not None:
            films = Film.objects.filter(
                title__icontains=q
            ) | Film.objects.filter(
                genre__icontains=q
            )

        for film in films:
            if Rental.objects.filter(film=film, return_date__isnull=True).exists():
                film.stock = False
            else:
                film.stock = True

        return render(request, 'films/list.html', { 
            'films':films,
            'users': users})
    
    return redirect('home')

def film_add(request):
    if request.user.is_authenticated:
        form = FilmForm(request.POST or None)
        if request.method =='POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Film dodany")
                return redirect('home')
        else:
            return render(request, 'films/form.html', {'form':form})
        return render(request, 'films/form.html', {'form':form})
    else:
        return redirect('home')


def film_edit(request, pk):
    if request.user.is_authenticated:
        update_it = Film.objects.get(id=pk)
        form = FilmForm(request.POST or None, instance=update_it)
        if form.is_valid():
            form.save()
            messages.success(request, "Film zaktualizowany")
            return redirect('film_list')
        else:
            return render(request, 'films/form.html', {'form': form})
    else:
        return redirect('home')

def film_remove(request, pk):
    if request.user.is_authenticated:
        delete_it = Film.objects.get(id=pk)
        if Rental.objects.filter(film=delete_it, return_date__isnull=True).exists() is False:
            delete_it.delete()
            messages.success(request, "Film usunięty")
        else: 
            messages.success(request, "Film został wypożyczony")
        return redirect('film_list')
    else:
        return redirect('home')

def film_rent(request, pk):
    if request.user.is_authenticated:
        if Rental.objects.filter(user=request.user, return_date__isnull=True).count() >= 3:
            messages.success(request, "Użytkownik przekroczył limit wypożyczeń")
            return redirect('film_list')

        film = Film.objects.get(id=pk)
    
        if Rental.objects.filter(user=request.user, film=film, return_date__isnull=True).exists() == False:
            Rental.objects.create(user=request.user, film=film)
            messages.success(request, "Film wypożyczony")
        else:
            messages.success(request, "Film już został wypożyczony wcześniej")
        return redirect('film_list')
    else:
        return redirect('home')

def film_rent_as(request, film, user):
    if request.user.is_authenticated:
        user = User.objects.get(id=user)
        if Rental.objects.filter(user=user, return_date__isnull=True).count() >= 3:
            messages.success(request, "Użytkownik przekroczył limit wypożyczeń")
            return redirect('film_list')

        film = Film.objects.get(id=film)
        if Rental.objects.filter(user=user, film=film, return_date__isnull=True).exists() == False:
            Rental.objects.create(user=user, film=film)
            messages.success(request, "Film wypożyczony")
        else:
            messages.success(request, "Film już został wypożyczony wcześniej")
        return redirect('film_list')
    else:
        return redirect('home')

def film_return(request, pk):
    if request.user.is_authenticated:
        update_it = Rental.objects.get(id=pk)
        update_it.return_date = now().date()
        update_it.save()
        messages.success(request, "Film zwrócony")
        return redirect('rental_list')
    else:
        return redirect('home')

def rental_list(request):
    if request.user.is_authenticated:
        rentals = Rental.objects.all().order_by("-id")
        users = User.objects.all()
        q = request.GET.get('search', '')
        if q:
            rentals = rentals.filter(
                Q(user__username__icontains=q) |
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q) |
                Q(film__title__icontains=q) |
                Q(film__genre__icontains=q)
            )
            
        
        return render(request, 'rentals/list.html', {
             'rentals':rentals,
             'users':users
             })
    else:
        return redirect('home')
    return redirect('home')

def rental_list_active(request):
    if request.user.is_authenticated:
        rentals = Rental.objects.filter(return_date__isnull=True).order_by("-id")
        users = User.objects.all()
        q = request.GET.get('search', '')
        if q:
            rentals = rentals.filter(
                Q(user__username__icontains=q) |
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q) |
                Q(film__title__icontains=q) |
                Q(film__genre__icontains=q)
            )
            
        
        return render(request, 'rentals/list.html', {
             'rentals':rentals,
             'users':users
             })
    else:
        return redirect('home')
    return redirect('home')

def rental_list_user(request, pk):
    if request.user.is_authenticated:
        user = User.objects.get(id=pk)
        users = User.objects.all()
        rentals = Rental.objects.filter(user=user, return_date__isnull=True).order_by("-id")
        q = request.GET.get('search', '')
        if q:
            rentals = rentals.filter(
                Q(user__username__icontains=q) |
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q) |
                Q(film__title__icontains=q) |
                Q(film__genre__icontains=q)
            )

        return render(request, 'rentals/list.html', {
             'rentals':rentals,
             'users':users
             })
    else:
        return redirect('home')
    return redirect('home')
# validated function

def function(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('home')
