from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm
from .models import Post

def post_list(request):
    # adding the paginator
    object_list = Post.published.all()
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
                                                   'page': page})

def post_detail(request, year, month, day, post):
    # this function retrieves the object that matches the given parameters or an
    # HTTP 404 exception
    post = get_object_or_404(Post, slug=post, 
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})

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
    if request.method == 'POST':
        # Form was submitted using POST
        form = EmailPostForm(request.POST) # creates an object of the class we defined
        # in the forms file with the request.POST data
        if form.is_valid():
            # Form fields passed the validation
            cd = form.cleaned_data # a dictionary of form fields and the their values
            # send the email
    else: # Form was not submitted using POST so we display an empty Form
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 
                                                        'form': form})