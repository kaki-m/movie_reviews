from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

#アプリが多数ある時にわかるように名前をつける
app_name="polls"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path("<int:pk>/",
         views.DetailView.as_view, name="detail"),
    path("<int:pk>/results/",
         views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote",
         views.vote, name="vote"),
    path('signup/', views.signupView, name='signup'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('user/', views.userView, name='user'),
    path('other/', views.otherView, name='other'),
    path('movies/', views.moviesView, name='movies'),
    path("movies/<int:pk>",views.movieReviewView, name='reviews'),
    path('write_review/', views.writeReviewView, name='write_review'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
