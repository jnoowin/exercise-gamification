from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import ListView
from bootstrap_modal_forms.generic import BSModalCreateView
from friendship.models import Friend, Follow
from .models import Workout, Dashboard, QuestCompleted
from .forms import WorkoutForm
from .utils import get_quest_tweet
import json
import datetime

'''
Title: Django Bootstrap Modal Forms
See also: new-workout.html
https://pypi.org/project/django-bootstrap-modal-forms/
'''
class WorkoutEntryView(BSModalCreateView):
    template_name = 'exercise/new-workout.html'
    model = Workout
    form_class = WorkoutForm
    success_message = 'Success: New workout logged.'
    success_url = reverse_lazy('exercise:dashboard')

    def form_valid(self, form):
        if not self.request.is_ajax() and self.request.user.is_authenticated:
            dashboard = Dashboard.objects.get(user=self.request.user)
            dashboard.duration += form.instance.duration
            dashboard.calories += form.instance.calories
            dashboard.progress += form.instance.duration + form.instance.calories
            dashboard.progressTotal += form.instance.duration + form.instance.calories

            while dashboard.max_exp < dashboard.progress:
                dashboard.level += 1
                dashboard.progress -= dashboard.max_exp
                dashboard.max_exp *= dashboard.level

            dashboard.percentage = int(
                (dashboard.progress / dashboard.max_exp) * 100)
            dashboard.streak += 1
            dashboard.save()
            form.instance.user = self.request.user
            return super().form_valid(form)
        return HttpResponseRedirect(reverse('exercise:index'))


def index(request):
    return render(request, 'exercise/index.html', {})


def dashboard(request):
    # redirect to landing page if not authenticated
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('exercise:index'))

    # get current user dashboard and order activities by date
    dashboard = get_object_or_404(Dashboard, user=request.user)
    workout_list = request.user.workout_set.all().order_by('-date')

    # convert workout date to display friendly format
    for workout in workout_list:
        workout.date = workout.date.strftime('%m/%d/%Y, %I:%M')
        workout.duration = str(datetime.timedelta(
            minutes=workout.duration))[:-3]

    # get quest completion status
    qc = QuestCompleted.objects.get(user=request.user)

    # check if yesterday's quest was completed + is new day to reset completed status
    if qc.completed and qc.is_new_day():
        qc.completed = False
        qc.save()

    # get current daily quest
    quest = get_quest_tweet()

    return render(request, 'exercise/dashboard.html', {
        'duration': dashboard.duration,
        'calories': dashboard.calories,
        'streak': dashboard.streak,
        'progress': dashboard.progress,
        'percentage': dashboard.percentage,
        'max_exp': dashboard.max_exp,
        'level': dashboard.level,
        'workout_list': workout_list,
        'quest_text': quest.text,
        'quest_url': 'https://twitter.com/twitter/statuses/' + str(quest.id),
        'completed': qc.completed,
    })


def social(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('exercise:index'))

    followers = Follow.objects.followers(request.user)
    following = Follow.objects.following(request.user)

    return render(request, 'exercise/social.html', {
        'num_followers': len(followers),
        'num_following': len(following),
        'followers': followers,
        'following': following,
    })


def leaderboard(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('exercise:index'))

    following = Follow.objects.following(request.user)
    user_list = Dashboard.objects.all().order_by('-progressTotal')

    dashboard = get_object_or_404(Dashboard, user=request.user)
    accountowner = dashboard.user

    Follow_dash_list = []  # query list

    for d in user_list:  # itterate through the ordered list first
        for u in following:  # compare names of those followed
            if d.user == u or d.user == accountowner:  # check for account owners name
                if d not in Follow_dash_list:
                    # ordered list of querys for follow leaderboard
                    Follow_dash_list.append(d)

    return render(request, 'exercise/leaderboard.html', {
        'user_list': user_list,
        'following': following,
        'Follow_dash_list': Follow_dash_list
    })


class SearchListView(ListView):
    template_name = 'exercise/search.html'
    context_object_name = 'user_dict'

    def get_queryset(self):
        query = self.request.GET.get('q')
        user_list = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
        following_list = Follow.objects.following(self.request.user)
        user_dict = {
            user: False for user in user_list if user.username != self.request.user.username}

        for followed in following_list:
            if followed in user_dict:
                user_dict[followed] = True
        return user_dict


'''
Title: Django-friendship
https://github.com/revsys/django-friendship'''
def follow(request):
    response = HttpResponse()
    if request.method == 'POST':
        username = json.loads(request.body.decode("utf-8"))['username']
        follow = json.loads(request.body.decode("utf-8"))['follow']
        user = User.objects.get(username=username)

        if user:
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('exercise:index'))

            if follow:
                Follow.objects.add_follower(request.user, user)
                response.status_code = 200
                return response
            else:
                Follow.objects.remove_follower(request.user, user)
                response.status_code = 200
                return response

    response.status_code = 500
    return response

def complete(request):
    if request.method == 'POST' and request.user.is_authenticated:
        qc = QuestCompleted.objects.get(user=request.user)
        qc.completed = True
        qc.save()

        dashboard = Dashboard.objects.get(user=request.user)
        dashboard.progress += dashboard.level * 50
        dashboard.progressTotal += dashboard.level * 50

        while dashboard.max_exp < dashboard.progress:
            dashboard.level += 1
            dashboard.progress -= dashboard.max_exp
            dashboard.max_exp *= dashboard.level

        dashboard.percentage = int(
            (dashboard.progress / dashboard.max_exp) * 100)
        dashboard.save()
    return HttpResponseRedirect(reverse('exercise:dashboard'))

def nearby_gyms(request):
    return render(request, 'exercise/gyms.html', {'API_KEY': 'AIzaSyAgFwkvm4tOO_D0LN8tNtUJqramdGWCIvI'})
