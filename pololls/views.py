from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Choice, Question

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'pololls/index.html'
    temp_name = 'pololls/header.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'pololls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'pololls/results.html'


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'pololls/detail.html', {
            'question': p,
            'error_message': "You didn't select any choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('results', args=(p.id,)))
