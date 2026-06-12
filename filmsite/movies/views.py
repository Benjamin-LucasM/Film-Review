from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.decorators import login_required
from datetime import datetime

def log(request, message):
    ip = request.META.get('REMOTE_ADDR')
    with open("log.txt", "a") as file:
        file.write(f"{datetime.now()} - {ip} - {message}\n")

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

class SimpleSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = movie.reviews.all()
    form = ReviewForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            log(request, f"review added from {request.user.username} on {pk}")
            return redirect('movies:detail', pk=pk)

    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'reviews': reviews,
        'form': form,
    })

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'genre', 'year', 'director', 'description', 'poster']

@login_required
def add_movie(request):
    if not request.user.is_superuser:
        return redirect('/')
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            log(request, f"Movie added: {request.POST.get('title')} by {request.user.username}")
            return redirect('/')
    else:
        form = MovieForm()
    return render(request, 'movies/add_movie.html', {'form': form})

@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user.is_superuser:
        log(request, f"Review deleted by admin: review id {pk}")
        review.delete()
    return redirect('movies:detail', pk=review.movie.pk)

def signup(request):
    if request.method == 'POST':
        form = SimpleSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            log(request, f"new user: {user.username}")
            return redirect('/')
    else:
        form = SimpleSignupForm()
    return render(request, 'registration/signup.html', {'form': form})