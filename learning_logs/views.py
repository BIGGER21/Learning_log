from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from .models import Topic,Entry
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """display all theme"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    #topics = Topic.objects.filter(owner=user).order_by('date_added')
    context = {'topics':topics}
    return render(request,'learning_logs/topics.html',context)

@login_required
def topic(request,topic_id):
    """display a single theme and it`s all items"""
    topic = Topic.objects.get(id=topic_id)
    """ensure the requested theme belong to current user"""
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('date_added')
    context = {'topic':topic,'entries':entries}
    return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    """add a new theme"""
    if request.method != 'POST':
        """not submit data:create a new form"""
        form = TopicForm()
    else:
        """POST submitted data to manage"""
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form':form}
    return render(request,'learning_logs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    """add a new entry in a certain topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        """not post data,create a null form"""
        form = EntryForm
    else:
        """manage the posted data"""
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))

    context = {'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    """edit existed items """
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    """ensure the requested theme belong to current user"""
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        """first request,use current item to fill the form"""
        form = EntryForm(instance=entry)
    else:
        """get the data from the POST and deal with it"""
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))

    context = {'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)

@login_required
def del_entry(request,entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    entry.delete()
    return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))












