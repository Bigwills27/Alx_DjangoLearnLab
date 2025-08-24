from django.views.generic import (
    ListView as DjangoListView,
    DetailView as DjangoDetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CustomUserCreationForm, UserUpdateForm, CommentForm, PostForm
from django.urls import reverse, reverse_lazy
from .models import Comment, Post, Like, PostView, Category
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages


# User-related views
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, "blog/profile.html", {"u_form": u_form})


# Post views
class PostListView(DjangoListView):
    model = Post
    template_name = "blog/post_list.html"  # Specify the template to use
    context_object_name = "posts"
    ordering = ["-published_date"]  # Order posts by the published date (newest first)
    paginate_by = 5  # Show 5 posts per page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add popular tags to context
        from django.db.models import Count
        context['popular_tags'] = Post.tags.most_common()[:10]
        # Add recent comments
        context['recent_comments'] = Comment.objects.select_related('post', 'author').order_by('-created_at')[:5]
        return context


class PostDetailView(DjangoDetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(post=self.object).order_by(
            "-created_at"
        )
        context["comment_form"] = CommentForm()
        
        # Add like status and count
        if self.request.user.is_authenticated:
            context["user_has_liked"] = Like.objects.filter(
                user=self.request.user, post=self.object
            ).exists()
        context["like_count"] = self.object.likes.count()
        
        return context

    def get(self, request, *args, **kwargs):
        # Track post views
        response = super().get(request, *args, **kwargs)
        post = self.get_object()
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Create or get view record
        if request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=request.user,
                post=post,
                ip_address=ip
            )
        else:
            PostView.objects.get_or_create(
                post=post,
                ip_address=ip,
                defaults={'user': None}
            )
        
        # Update post view count
        post.view_count = post.post_views.count()
        post.save(update_fields=['view_count'])
        
        return response

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect("post-detail", pk=post.pk)
        return self.get(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author to the logged-in user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user  # Ensure author is the logged-in user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return (
            self.request.user == post.author
        )  # Only allow authors to update their posts


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")  # Redirect after deletion

    def test_func(self):
        post = self.get_object()
        return (
            self.request.user == post.author
        )  # Only allow authors to delete their posts


# Comment views
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"  # Create this template if it doesn't exist

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs["post_id"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.kwargs["post_id"]})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = (
            self.object.post
        )  # Assuming Comment model has a ForeignKey to Post
        return context

    def get_success_url(self):
        return reverse(
            "post-detail", kwargs={"pk": self.object.post.pk}
        )  # Redirect to post detail after updating comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author  # Only the author can edit


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        post = self.get_object().post
        return reverse_lazy("post-detail", kwargs={"pk": post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author  # Only the author can delete


# Tagging and Search Functionality
class PostSearchView(DjangoListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Post.objects.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(tags__name__icontains=query)
            ).distinct()
        return Post.objects.none()


class PostByTagListView(DjangoListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        slug = self.kwargs.get("tag_slug")
        return Post.objects.filter(tags__slug=slug)


# Like/Unlike functionality
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        # If like already exists, remove it (unlike)
        like.delete()
        liked = False
        messages.info(request, 'You unliked this post.')
    else:
        liked = True
        messages.success(request, 'You liked this post!')
    
    # Return JSON response for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'like_count': post.likes.count()
        })
    
    return redirect('post-detail', pk=pk)


# Category views
class PostByCategoryListView(DjangoListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        category = get_object_or_404(Category, slug=slug)
        return Post.objects.filter(category=category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        context['category'] = get_object_or_404(Category, slug=slug)
        return context
