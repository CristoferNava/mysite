from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from taggit.models import Tag
from .forms import EmailPostForm, CommentForm
from .models import Post, Comment

def post_list(request, tag_slug=None):
    # adding the paginator
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
        # we use the __in field lookup
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page') # indicates the current page number
    try:
        posts = paginator.page(page) # obtains the objects for the desired page
    except PageNotAnInteger:
        # If page is not a integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts,
                                                   'page': page,
                                                   'tag': tag,})

def post_detail(request, year, month, day, post):
    # this function retrieves the object that matches the given parameters or an
    # HTTP 404 exception
    post = get_object_or_404(Post, slug=post, 
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True) # post.comments from the related name in the model
    new_comment = None
    
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create a Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,})

# we can write the post_list view as class-based view to use the generic ListView
# this base view allows us to list objects of any kind
from django.views.generic import ListView

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    # path('', views.PostListView.as_view(), name='post_list')
    # {% include "pagination.html" with page=page_obj %}

def post_share(request, post_id):
    ''' Handles the form and sends an email when it's successfully submitted.'''
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted using POST
        form = EmailPostForm(request.POST) # creates an object of the class we defined
        # in the forms file with the request.POST data
        if form.is_valid():
            # Form fields passed the validation
            cd = form.cleaned_data # a dictionary of form fields and the their values
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # post_url build a complete URL, including the HTTP schema and hostname
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else: # Form was not submitted using POST so we display an empty Form
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,     
                                                    'form': form,
                                                    'sent': sent,})