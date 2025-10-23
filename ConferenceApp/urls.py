from django.urls import path
from .views import *
#from . import views

urlpatterns=[
    #path("liste/",views.all_conference,name="conference_liste"),
    path("liste/",ConferenceListe.as_view(),name="conference_liste"),
    path("details/<int:pk>/",ConferenceDetail.as_view(),name="conference_detail"),
    path("form/",Conferencecreate.as_view(),name="conference_create"),
    path("<int:pk>/update/",conference_update.as_view(),name="conference_update"),
    path("<int:pk>/delete/>",ConferenceDelete.as_view(),name="conference_delete"),
]