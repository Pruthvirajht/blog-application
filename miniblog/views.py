from django.shortcuts import render,HttpResponseRedirect
from .forms import SignupForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group

# Create your views here.
#HOME
def home(request):
    post = Post.objects.all()
    return render(request,'miniblog/home.html',{'posts':post})

#ABOUT
def about(request):
    return render(request,'miniblog/about.html')

#CONTACT
def contact(request):
    return render(request,'miniblog/contact.html')

#DASHBOARD
def dashboard(request):
    if request.user.is_authenticated:
        post = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request,'miniblog/dashboard.html',{'posts':post,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

#LOGOUT
def user_logut(request):
    logout(request)
    return HttpResponseRedirect('/')

#SIGN_UP
def user_signup(request):
    if request.method =='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratualations!!! You have become an Author')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignupForm()
    return render(request,'miniblog/signup.html' ,{'form':form})

#LOGIN
def user_login(request):
    if not request.user.is_authenticated:

        if request.method == 'POST':
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username = uname,password = upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Loggedin Successfully!!!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request,'miniblog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')


#detail
def detail(request, pk):
    post = Post.objects.get(id=pk)
    return render(request, 'miniblog/detail.html', {'pk':post})

#Add New Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                author = form.cleaned_data['author']
                desc = form.cleaned_data['desc']
                dop = form.cleaned_data['dop']
                pst = Post(title=title,author=author,desc=desc,dop=dop)
                pst.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request,'miniblog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

#Update Post
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request,'miniblog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

#Delete Post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi =Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

