from django.shortcuts import render,HttpResponseRedirect
from django.views.generic import CreateView,UpdateView,DeleteView,ListView,DetailView,View,TemplateView
from App_Blog.models import Blog,Comment,Likes
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin 
import uuid
from App_Blog.forms import CommentForm
from django.utils.text import slugify
from django.utils.text import slugify
import uuid

class MyBlog(LoginRequiredMixin,TemplateView):
    template_name='App_Blog/my_blogs.html'


class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = "App_Blog/create_blog.html"
    fields = ['blog_title', 'blog_content', 'blog_image']

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user 
        title = blog_obj.blog_title

        # Title ke slugify kore unique slug generate kora
        blog_obj.slug = slugify(title) + "-" + str(uuid.uuid4())

        # Blog save kora
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))

    
    
class BlogList(ListView):
    context_object_name='blogs'
    model=Blog
    template_name='App_Blog/blog_list.html'


# views.py
@login_required
def blog_details(request, slug):
    
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return HttpResponseRedirect(reverse('App_Blog:blog_list'))
    
    # Debugging line to check if slug is coming through 
    comment_form = CommentForm()
    already_liked = Likes.objects.filter(blog=blog, user=request.user)
    liked = bool(already_liked)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug': slug}))
    
    return render(request, 'App_Blog/blog_details.html', {
        'blog': blog,
        'comment_form': comment_form,
        'liked': liked
    })

    
   



@login_required
def liked(request,pk):
    blog=Blog.objects.get(pk=pk)
    user=request.user
    already_liked=Likes.objects.filter(blog=blog,user=user)
    if not already_liked:
        liked_post=Likes(blog=blog,user=user)
        liked_post.save()
        return HttpResponseRedirect(reverse('App_Blog:blog_details',kwargs={'slug':blog.slug}))
    
@login_required
def unliked(request,pk):
    blog=Blog.objects.get(pk=pk)
    user=request.user
    already_liked=Likes.objects.filter(blog=blog,user=user) 
    already_liked.delete()    
    return HttpResponseRedirect(reverse('App_Blog:blog_details',kwargs={'slug':blog.slug}))
         
class UpdateBlog(LoginRequiredMixin,UpdateView):
    model=Blog
    fields=('blog_title','blog_content','blog_image')
    template_name='App_Blog/edit_blog.html'
    
    def get_success_url(self):
        return reverse('App_Blog:blog_details',kwargs={'slug':self.object.slug})

class DeleteBlog(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'App_Blog/delete_blog.html'
    success_url = reverse_lazy('App_Blog:blog_list')

    def get_queryset(self):
        # Limit deletion to the logged-in user's own blogs
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)
