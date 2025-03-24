from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm

def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "chatboard/post_list.html", {"posts": posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Filter only top-level comments (requires Comment.parent field)
    top_level_comments = post.comments.filter(parent__isnull=True)
    comment_form = CommentForm()
    return render(request, "chatboard/post_detail.html", {
        "post": post,
        "comment_form": comment_form,
        "top_level_comments": top_level_comments,
    })

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.created_at = timezone.now()
            new_post.save()
            return redirect("post_detail", pk=new_post.pk)
    else:
        form = PostForm()
    return render(request, "chatboard/post_create.html", {"form": form})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.created_at = timezone.now()
            new_comment.save()
    return redirect("post_detail", pk=post.pk)

@login_required
def add_reply(request, pk):
    parent_comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = parent_comment.post
            new_reply.parent = parent_comment  # Make sure Comment model has a self-referential field named "parent"
            new_reply.created_at = timezone.now()
            new_reply.save()
    return redirect("post_detail", pk=parent_comment.post.pk)

def profile(request, username):
    """Renders the profile page for a given user."""
    user_obj = get_object_or_404(User, username=username)
    return render(request, "chatboard/profile.html", {"profile_user": user_obj})

@login_required
def customize_profile(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "")
        location = request.POST.get("location", "")
        profile_picture = request.FILES.get("profile_picture")
        image_url = request.POST.get("image_url", "")
        
        # Update the User model
        request.user.first_name = full_name  # or split into first_name and last_name as needed
        request.user.save()
        
        # Get or create the Profile for the user.
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.location = location
        if profile_picture:
            profile.image = profile_picture
            # Optionally, clear image_url if a file was uploaded.
            profile.image_url = ""
        elif image_url:
            profile.image_url = image_url
            # Optionally, clear the image field if a URL is provided.
            profile.image = None
        profile.save()
        
        return redirect(reverse("profile", kwargs={"username": request.user.username}))
    else:
        return redirect("profile", username=request.user.username)
