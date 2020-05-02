import pandas as pd
from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go

from main_app.models import Dish, Rating
from django.db.models import Avg
from main_app.views.views_utils import get_dining_halls, get_diets, get_allergens, get_roles, get_schools, \
    get_grad_years, save_dish_rating, get_dish
from main_app.views.views_constants import num_results


def advanced_search_view(request):
    search_results = get_most_popular_results(request)

    response = {
        'form': request.POST,
        'dining_halls': get_dining_halls(),
        'diets': get_diets(),
        'allergens': get_allergens(),
        'roles': get_roles(),
        'schools': get_schools(),
        'grad_years': get_grad_years(),
        'results': search_results,
        'plot_div': get_plot(search_results)
    }

    return render(request, 'advanced_search.html', response)


def get_search_results(request):
    results = Dish.objects.all()

    if request.method == "POST":
        if request.POST.get('rating'):
            save_dish_rating(request, get_dish(request.POST.get('dish')))
        else:
            if request.POST['dining_hall'] != 'any':
                results = results.filter(dining_hall=request.POST['dining_hall'])

            if request.POST['dish_name']:
                results = results.filter(name=request.POST['dish_name'])

            if request.POST['diet'] != 'any':
                results = results.filter(dietaryrestrictionsofdish__dietary_restriction__name=request.POST['diet'])

            if request.POST.getlist('allergens') != ['any']:

                results = results.exclude(
                    dietaryrestrictionsofdish__dietary_restriction__name__in=request.POST.getlist('allergens')
                )

    return pd.DataFrame(results.values())


def get_most_popular_results(request):
    result_rows = get_search_results(request)
    avg_dish_ratings = get_avg_dish_ratings(request)

    if result_rows.empty or avg_dish_ratings.empty:
        results = []
    else:
        results = pd.merge(
            result_rows,
            avg_dish_ratings,
            left_on='id',
            right_on='dish_id',
        ).sort_values(
            'avg_rating',
            ascending=False
        ).head(num_results).to_dict('records')

    return results


def get_avg_dish_ratings(request):
    avg_ratings = Rating.objects.filter(dish__isnull=False)

    if request.method == "POST" and not request.POST.get('rating'):

        if request.POST['role'] != 'any':
            avg_ratings = avg_ratings.filter(user__role=request.POST['role'])

        if request.POST['school'] != 'any':
            avg_ratings = avg_ratings.filter(user__school=request.POST['school'])

        if request.POST['grad_year'] != 'any':
            if request.POST['grad_year'] == 'NA':
                avg_ratings = avg_ratings.filter(user__grad_year__isnull=True)
            else:
                avg_ratings = avg_ratings.filter(user__grad_year=request.POST['grad_year'])

    return pd.DataFrame(
        avg_ratings.values('dish_id')
        .annotate(avg_rating=Avg('forks'))
        .order_by('-avg_rating')
    )


def get_plot(results):
    data = [go.Bar(
            x=[dish['avg_rating'] for dish in reversed(results)],
            y=[f"{dish['name']}   <br> {dish['dining_hall_id']}" for dish in reversed(results)],
            text=[round(dish['avg_rating'], 2) for dish in reversed(results)],
            textposition='auto',
            marker=dict(
                color='#7ABDFF',
                line=dict(color='dodgerblue', width=3)
            ),
            orientation='h',
    )]

    layout = go.Layout(
        yaxis=dict(ticksuffix="   "),
        title='Most Popular Dishes',
        margin=dict(pad=5),
        paper_bgcolor='rgb(248, 248, 255)',
    )

    fig = go.Figure(data=data, layout=layout)
    return plot(
        fig,
        output_type='div',
    )
