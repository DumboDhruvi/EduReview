from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm, ReviewForm, DiscussionForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Course, Subject

def home(request):
    subjects = Subject.objects.all()
    user = request.user if request.user.is_authenticated else None
    return render(request, 'home.html', {
        'user': user,
        'subjects': subjects,
    })

def search(request):
    query = request.GET.get('query', '')  # Get the search query
    mode = request.GET.get('mode', 'text')  # Get the search mode, default to 'text'

    courses = []  # Initialize an empty list for search results

    if mode == 'text' and query:
        # Text mode: search by course name
        courses = Course.objects.filter(course_name__icontains=query)
    
    elif mode == 'subject' and query:
        # Subject mode: search by subject name
        courses = Course.objects.filter(subjects__name__icontains=query)
    
    elif mode == 'institution' and query:
        # Institution mode: search by educational institution
        courses = Course.objects.filter(institution__name__icontains=query)
    
    # If no query is provided, display only the search box
    context = {
        'query': query,
        'courses': courses,
        'mode': mode
    }
    
    return render(request, 'search.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home after signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home after login
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')  # Redirect to home after logout

def course_detail(request, course_name):
    course = get_object_or_404(Course, course_name=course_name)
    reviews = course.reviews.all()
    discussions = course.discussions.all()

    # Initialize both forms
    review_form = ReviewForm()
    discussion_form = DiscussionForm()

    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        if 'review' in request.POST:  # Handle the review form
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.course = course
                review.save()
                return redirect('course_detail', course_name=course.course_name)

        elif 'discussion' in request.POST:  # Handle the discussion form
            discussion_form = DiscussionForm(request.POST)
            if discussion_form.is_valid():
                discussion = discussion_form.save(commit=False)
                discussion.user = request.user
                discussion.course = course
                discussion.save()
                return redirect('course_detail', course_name=course.course_name)

    # Calculate the average rating
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    # Render the page with context
    context = {
        'course': course,
        'reviews': reviews,
        'discussions': discussions,
        'review_form': review_form,
        'discussion_form': discussion_form,
        'average_rating': average_rating,
    }

    return render(request, 'course_detail.html', context)