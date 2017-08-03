from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response,redirect, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import register
from django.utils import timezone
from django.views import generic
from django.template import RequestContext
from django.db.models import F, Sum
from django.core.exceptions import ObjectDoesNotExist

from dashboard.views import getMessageCount
from .models import Choice, Poll, Voter
from .forms import QuestionForm, ChoiceForm
from django.forms import modelform_factory

@login_required(login_url='/login')
def index(request):
    latest_poll_list = Poll.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')

    return render_to_response('index.html', {'latest_poll_list': latest_poll_list, 'messagecount': getMessageCount()}, RequestContext(request))

def detail(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
        request.session['question_id'] = poll_id
        totalvotes = Choice.objects.filter(poll__exact=poll).aggregate(total_votes=Sum(F('votes')))
        if Voter.objects.filter(poll_id=poll_id, user_id=request.user.id).exists() or request.user.is_superuser:
            return render(request, 'results.html', {
                'poll': poll,
                'messagecount': getMessageCount(),
                'votecount': 0,
                'total_votes': totalvotes,
            })
    except ObjectDoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'detail.html', {'poll': poll, 'messagecount': getMessageCount(), 'votecount': 0})


def results(request, poll_id):
    messagecount = getMessageCount()
    poll = Poll.objects.get(pk=poll_id)

    totalvotes = Choice.objects.filter(poll__exact=poll).aggregate(total_votes=Sum(F('votes')))

    return render(request, 'results.html', {'poll': poll, 'messagecount': messagecount, 'total_votes': totalvotes})

@login_required(login_url='/login')
def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    if Voter.objects.filter(poll_id=poll_id, user_id=request.user.id).exists():
        return render(request, 'detail.html', {
            'poll': p,
            'error_message': "Sorry, but you have already voted.",
            'messagecount': getMessageCount()
        })
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
            'messagecount': getMessageCount()
        })
    else:
        selected_choice.votes = F('votes') +1
        selected_choice.save()
        v = Voter(user=request.user, poll=p)
        v.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(p.id,)))

@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='/login')
def add_poll(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            question = form.cleaned_data['question']
            form.save()
            request.session['question_id'] = Poll.objects.get(question__exact=question).id
            # Now call the index() view.
            # The user will be shown the homepage.
            return redirect(add_choice)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = QuestionForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'add_poll.html', {'form': form, 'messagecount': getMessageCount()})

@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='/login')
def add_choice(request):
    question_id = request.session['question_id']
    if request.method == 'POST':
        form = ChoiceForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save()

            # Now call the index() view.
            # The user will be shown the homepage.
            return redirect(add_choice)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.

        form = ChoiceForm(initial={'poll': Poll.objects.get(id__exact=question_id)})

        # Bad form (or form details), no form supplied...
        # Render the form with error messages (if any).
    return render(request, 'add_choices.html', {'form': form, 'messagecount': getMessageCount()})

@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='/login')
def delete_poll(request, poll_id):
    get_object_or_404(Poll, pk=poll_id).delete()
    return redirect(index)

@register.filter
def customFilter(votes, total):
    return (votes / total) * 100
