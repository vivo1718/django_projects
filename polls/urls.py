from django.urls import path
from . import views

urlpatterns = [
    path('', views.poll_view, name='poll_view'),
    path('vote/', views.vote_submit, name='vote_submit'),
    path('results/<int:question_id>/', views.vote_results, name='vote_results'), # Updated path
]
