from django.urls import path, include

from . import views

app_name = 'exercise'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('new-workout/', views.WorkoutEntryView.as_view(), name='new_workout'),
    path('social/', views.social, name='social'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('follow/', views.follow, name='follow'),
    path('complete/', views.complete, name='complete'),
    path('nearby-gyms/', views.nearby_gyms, name='nearby-gyms'),
]
