from django.urls import path

from .import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:course_id>/', views.detail, name='detail'),
    path('<str:course_id>/<str:plot_id>/', views.results, name='results'),
    path('<str:course_id>/<str:plot_id>/<str:act_id>/', views.plot, name='plot'),
    path('<str:course_id>/<str:plot_id>/<str:act_id>/<str:search_id>/', views.new_plot, name='new_plot'),
]
