from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, Vote
from .forms import TopicForm, CommentForm
from django.contrib import messages
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

def topic_list(request):
    topics = Topic.objects.order_by('-created_at')
    return render(request, 'topic_list.html', {'topics': topics})

def topic_detail(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    comments = topic.comments.order_by('-created_at')
    comment_form = CommentForm()
    user_vote = topic.votes.filter(user=request.user).first() if request.user.is_authenticated else None
    return render(request, 'topic_detail.html', {
        'topic': topic,
        'comments': comments,
        'comment_form': comment_form,
        'user_vote': user_vote
    })

@login_required
def topic_vote(request, slug, vote_type):
    topic = get_object_or_404(Topic, slug=slug)
    is_upvote = vote_type == 'up'  # or some other logic

    vote, created = Vote.objects.get_or_create(
        topic=topic,
        user=request.user,
        defaults={'is_upvote': is_upvote}
    )

    if not created:
        vote.is_upvote = is_upvote
        vote.save()

    return redirect('blog:topic_detail', slug=slug)


@login_required
def add_comment(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.topic = topic
            new_comment.user = request.user
            new_comment.save()
    return redirect('blog:topic_detail', slug=slug)

@login_required
def topic_create(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            messages.success(request, "Topic created successfully.")
            return redirect('blog:topic_detail', slug=topic.slug)
    else:
        form = TopicForm()
    return render(request, 'topic_form.html', {'form': form, 'title': 'Create Topic'})

@login_required
def edit_topic(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    if topic.author != request.user:
        messages.error(request, "You are not authorized to edit this topic.")
        return redirect('blog:topic_detail', slug=slug)

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, "Topic updated successfully.")
            return redirect('blog:topic_detail', slug=topic.slug)
    else:
        form = TopicForm(instance=topic)
    return render(request, 'topic_form.html', {'form': form, 'title': 'Edit Topic'})

@login_required
def delete_topic(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    if topic.author != request.user:
        messages.error(request, "You are not authorized to delete this topic.")
        return redirect('blog:topic_detail', slug=slug)

    if request.method == 'POST':
        topic.delete()
        messages.success(request, "Topic deleted successfully.")
        return redirect('blog:topic_list')
    return render(request, 'topic_confirm_delete.html', {'topic': topic})

def test_view(request):
    topics = Topic.objects.order_by('-created_at')
    return render(request, 'test.html', {'topics': topics})

def news(request):
    topics = Topic.objects.order_by('-created_at')
    return render(request, 'news.html', {'topics': topics})

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        send_mail(
            subject=f"Contact Us Message from {name}",
            message=message,
            from_email=email,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )

        return HttpResponseRedirect(reverse('blog:contact_thanks'))

    return render(request, 'contact.html')

def about_view(request):
    return render(request, 'about.html')

def all_topics_view(request):
    topics = Topic.objects.all().order_by('-created_at')  # or any order you prefer
    return render(request, 'topics.html', {'topics': topics})