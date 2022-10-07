from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Question, Choice
from django.utils import timezone


# Create your views here.

def index(request):

    # q = Question();
    # q.question_text = "who are you?"
    # q.pub_date = timezone.now();
    # q.save();

    return HttpResponse("success")


def res(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    context = {'latest_question_list': latest_question_list}
    return render(request, 'index.html', context)



def detail(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    choices = Choice.objects.filter(question=question_id)
    return render(request, 'detail.html', {'question': question, 'choices':choices})



# ...
def vote(request, question_id):
    choice = request.POST['choice']
    print(choice);
    return HttpResponse('success');


