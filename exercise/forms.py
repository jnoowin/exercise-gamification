from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import Workout

class WorkoutForm(BSModalModelForm):
    date = forms.DateTimeField(
        error_messages={
            'invalid': 'Enter a valid date in MM/DD/YYYY HH:MM format.'
        }
    )

    class Meta:
        model = Workout
        fields = ['date', 'duration', 'workout_type', 'calories']
