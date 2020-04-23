import random
import string
import datetime
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fivecbites.settings")
django.setup()

from main_app.models import User
from main_app.ratings_script.user_constants import names, default_password, schools, roles


if __name__ == "__main__":
    today = datetime.datetime.today()

    for name in names:
        username = f"{name} {random.choice(string.ascii_uppercase)}."
        role = random.choice(roles)
        grad_year = random.choice(list(range(2020, 2024))) if role == 'student' else None
        User.objects.create(
            username=username,
            password=default_password,
            school=random.choice(schools),
            role=role,
            grad_year=grad_year,
            date_joined=today,
        )
