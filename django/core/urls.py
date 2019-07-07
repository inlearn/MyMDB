
from django.urls import path

from core import views

app_name='core'
urlpatterns=[
    path('',views.MovieList.as_view(),name='MovieList'),
    path('movie/<int:pk>',views.MovieDetail.as_view(),name='MovieDetail'),
    path('people',views.PersonList.as_view(),name='PersonList'),
    path('person/<int:pk>',views.PersonDetail.as_view(),name='PersonDetail'),
    path('movie/<int:movie_id>/vote',views.CreateVote.as_view(),name='CreateVote'),
    path('movie/<int:movie_id>/vote/<int:pk>',views.UpdateVote.as_view(),name='UpdateVote')
]