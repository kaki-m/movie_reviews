from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import Choice, Question
from django.template import loader
from django.urls import reverse

from django.views import generic
from django.utils import timezone

from .forms import SignupForm, LoginForm, ReviewForm
from django.contrib.auth import login,logout
from .models import CustomUser, Movie, Review
from django.db.models import Avg

# genericのlistViewはモデルオブジェクトのリストを表示する
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
            ]

# detailViewはオブジェクトの詳細ページを表示する
class DetailView(generic.DetailView):
    # 質問の詳細を見せるためのview
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question":question,
                "error_message": "You didn't select a choice",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
    
    return HttpResponseRedirect(reverse("polls:results", args=(question.id)))

# ここからログイン機能
def signupView(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            print('ユーザー登録ができました')
        else:
            print('ユーザー登録に失敗しました')
            print(form)
    else:
        form = SignupForm()
    
    param = {
        'form':form
    }

    return render(request, 'polls/signup.html',
                  param)
def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            # authenticationFormがget_userを持っているので、これでユーザー情報を取得できる
            user = form.get_user()
            if user:
                # ログイン状態にする関数
                login(request, user)
            else:
                print('userが受け取れませんでした')
        else:
            print('与えられた情報ではis_validを通過しませんでした')
    
    else:# ログインページのGETなどだったら
        form = LoginForm()
    param = {
        'form': form,
    }

    return render(request, 'polls/login.html', param)

def logoutView(request):
    logout(request)
    return render(request, 'polls/logout.html')

def userView(request):
    user = request.user
    print(user)
    params = {
        'user': user,
    }
    return render(request,'polls/user.html', params)

def otherView(request):
    users = CustomUser.objects.exclude(username=request.user.username)
    params = {
        'users': users,
    }
    return render(request, 'polls/other.html', params)

def moviesView(request):
    user = request.user
    movies = Movie.objects.all()

    # 映画の平均星数を出すために計算する
    for movie in movies:
        reviews = Review.objects.filter(movie=movie)
        if reviews.exists():
            avg_rating = reviews.aggregate(Avg('star_num'))['star_num__avg']
            movie.avg_star = round(avg_rating, 1)
            movie.reviews_count = reviews.count()
        else:
            movie.avg_star = 0.0
            movie.reviews_count = 0

    params = {
        'user': user,
        'movies': movies,
    }
    return render(request, 'polls/select_movie.html', params)

def movieReviewView(request,pk):
    user = request.user
    selected_movie = get_object_or_404(Movie, pk=pk)
    reviews = Review.objects.filter(movie=selected_movie)
    
    params = {
        'user':user,
        'movie': selected_movie,
        'movie_id': pk,
        'reviews': reviews,
    }
    return render(request, 'polls/movie_review.html', params)

def writeReviewView(request):
    user = request.user
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content_text = form.cleaned_data['content_text']
            star_num = form.cleaned_data['star_num']
            movie = form.cleaned_data['movie']
            writer = user
            review = Review(
                movie=movie,
                title=title,
                content_text=content_text,
                star_num=int(star_num),
                writer=writer)
            review.save()
            return redirect('../movies/'+str(movie.id))  # GETメソッドでのリダイレクト
    else:
        form = ReviewForm()
    params = {
        'user': user,
        'form': form,
    }
    return render(request, 'polls/write_review.html', params)