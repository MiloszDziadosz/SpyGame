from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import Room, Tempuser, Gametemp


class RoomForm(forms.Form):
    gt = forms.ModelChoiceField(queryset=Gametemp.objects.all(), label='Szablon Gry')
    room_name = forms.CharField()
    password = forms.CharField()
    nickname = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            'gt',
            'room_name',
            'password',
            'nickname',
            Submit('submit', 'Submit', css_class='btn btn-lg btn-primary btn-block', style='margin-top: 20px')
        )


class TempuserForm(forms.Form):
    nickname = forms.CharField()
    room = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            'room',
            'nickname',
            Submit('submit', 'Submit', css_class='btn-success', style='margin-top: 20px')
        )

