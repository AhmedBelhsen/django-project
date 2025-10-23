from django.shortcuts import get_object_or_404, render
from .models import Conference
from .forms import conference_form
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
# Create your views here.
def all_conference(req):
    conferences=Conference.objects.all()
    return render(req,'Conference/liste.html',{"liste":conferences})
#they are replaced by class-based views below
class ConferenceListe(ListView):
    model=Conference
    context_object_name="liste"
    ordering=["start_date"]
    template_name="Conference/list.html"

def conference_detail(request,id):
    conference = get_object_or_404(Conference, conference_id=id)
    return render(request,'Conference/details.html',{"conference":conference})
#they are replaced by class-based views below
class ConferenceDetail(DetailView):
    model=Conference
    context_object_name="conference"
    template_name="Conference/details.html"

class Conferencecreate(CreateView):
    model=Conference
    form_class= conference_form
    #fields= '__all__'
    template_name="Conference/conference_form.html"
    success_url=reverse_lazy("conference_liste")

class conference_update(UpdateView):
    model=Conference
    #fields='__all__'
    form_class=conference_form #one of the two options to display form
    template_name="Conference/conference_form.html"
    success_url=reverse_lazy("conference_liste")

class ConferenceDelete(DeleteView):
    model=Conference
    template_name="Conference/conference_confirm_delete.html"
    success_url=reverse_lazy("conference_liste")