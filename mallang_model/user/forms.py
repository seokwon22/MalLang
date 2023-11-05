from django import forms
from .models import Board

from .models import Diary

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['user_id', 'nickname', 'title', 'content', 'image', 'date']

class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['diarydate', 'diaryweather', 'diaryemoji', 'diarycontent', 'image']