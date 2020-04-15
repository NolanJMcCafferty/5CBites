from django.contrib.auth.forms import UserCreationForm
from main_app.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role', 'school', 'grad_year')
