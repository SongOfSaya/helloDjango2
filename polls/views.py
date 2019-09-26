from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from .models import Question
from django.template import loader
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list, }
    return render(request,'polls/index.html',context)


def detail(request, question_id):
    try:
        question = Question.objects.get(pk = question_id)
    except Question.DoesNotExist:
        raise Http404("您要的问题不存在")
    return render(request, 'polls/detail.html',{'question':question})


def results(request, question_id):
    response = "你正在查询问题 %s 的结果"
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("你正在为问题%s投票" % question_id)
