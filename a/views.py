from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.auth import authenticate,login as login_user,logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        utype = Usertype.objects.get(user=user).user_type
        return render(request,"a/index.html",{'utype':utype})
    else:
        return render(request,"a/index.html",{'message':'non auth'})
    
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        username = username.lower()
        email = request.POST.get("email")
        password = request.POST.get("password")
        usertype = request.POST.get("usertype")
        phoneno = request.POST.get("phoneno")
        print(phoneno)
        if usertype == "host":
            documentProof = request.FILES.get("documentProof")
            user = User.objects.filter(username=username)
            if user.exists():
                messages.error(request,"Username already taken!")
            elif User.objects.filter(email=email).exists():
                messages.error(request,"Email already taken!")
            elif Usertype.objects.filter(phone_no=phoneno).exists():
                messages.error(request,"Phone number already taken!")
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                usertype = Usertype.objects.create(user=user,user_type="host",document_proof=documentProof,phone_no=phoneno)
                messages.success("User created succesfully!")
        else:
            user = User.objects.filter(username=username)
            if user.exists():
                messages.error(request,"Username already taken!")
            elif User.objects.filter(email=email).exists():
                messages.error(request,"Email already taken!")
            elif Usertype.objects.filter(phone_no=phoneno).exists():
               messages.error(request,"Phone number already taken!")
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                usertype = Usertype.objects.create(user=user,user_type="attendee",phone_no=phoneno)
                messages.error(request,"Username created succesfully!")
            
    return render(request,"a/signup.html",{})
    
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        username = username.lower()
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login_user(request,user)
                return redirect('index')
            else:
                messages.error(request,"Invalid password!")
        else:
           messages.error(request,"Invalid username!")
        
    return render(request,"a/login.html",{})

def logout(request):
    logout_user(request)
    return redirect('index')

@login_required(login_url="login")
def addpost(request):
    user = User.objects.get(username=request.user)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        location = request.POST.get("location")
        ticket_fare = request.POST.get("ticketFare")
        datetime = request.POST.get("date")
        if Usertype.objects.get(user=request.user).user_type == "host":
            Post.objects.create(title=title,description=description,location=location,Ticket_fare=ticket_fare,author=user,event_date=datetime)
            messages.success(request,"Post added succesfully")
        else:
            messages.error(request,"You should not be here")
            return redirect("index")
    
    return render(request,"a/addpost.html",{})

def posts(request):
    posts = Post.objects.all()
    margin = Ticket.platform_fees/100
    for post in posts:
        post.adjusted_ticket_fare = (post.Ticket_fare * margin) + post.Ticket_fare 
    return render(request,"a/posts.html",{"posts":posts})

@login_required(login_url="login")
def elaborate(request,id):
    user = User.objects.get(username=request.user)
    post = Post.objects.get(id=id)
    now = timezone.now()
    likes = Like.objects.filter(post=post).count()
    dislikes = Dislike.objects.filter(post=post).count()
    margin = Ticket.platform_fees/100
    post.adjusted_ticket_fare = (post.Ticket_fare * margin) + post.Ticket_fare
    all_comments = Comment.objects.filter(post=post).exclude(author=user)
    u_comments = Comment.objects.filter(post=post,author=user)
    bookings = Ticket.objects.filter(event=post).count()
    if Ticket.objects.filter(event=post,buyer=user).exists():
        return render(request,"a/elaborate.html",{"post":post,"now":now,"likes":likes,"dislikes":dislikes,"all_comments":all_comments,"u_comments":u_comments,"bookings":bookings,"ub":True})     
    if Like.objects.filter(post=post,author=user).exists():
        return render(request,"a/elaborate.html",{"post":post,"now":now,"likes":likes,"dislikes":dislikes,"liked":"liked","all_comments":all_comments,"u_comments":u_comments,"bookings":bookings})    
    if Dislike.objects.filter(post=post,author=user).exists():
        return render(request,"a/elaborate.html",{"post":post,"now":now,"likes":likes,"dislikes":dislikes,"disliked":"disliked","all_comments":all_comments,"u_comments":u_comments,"bookings":bookings})   
    return render(request,"a/elaborate.html",{"post":post,"now":now,"likes":likes,"dislikes":dislikes,"all_comments":all_comments,"u_comments":u_comments,"bookings":bookings})

def like(request,id):
    post = Post.objects.get(id=id)
    if Like.objects.filter(post=post,author=request.user).exists():
        like = Like.objects.get(post=post,author=request.user)
        like.delete()
        return redirect("elaborate",id=id)
    else:
        like = Like.objects.create(post=post,author=request.user)
        if Dislike.objects.filter(post=post,author=request.user).exists():
            dislike = Dislike.objects.get(post=post,author=request.user)
            dislike.delete()
        
        return redirect("elaborate",id=id)

def dislike(request,id):
    post = Post.objects.get(id=id)
    if Dislike.objects.filter(post=post,author=request.user).exists():
        dislike = Dislike.objects.get(post=post,author=request.user)
        dislike.delete()
        return redirect("elaborate",id=id)
    else:
        dislike = Dislike.objects.create(post=post,author=request.user)
        if Like.objects.filter(post=post,author=request.user).exists():
            like = Like.objects.get(post=post,author=request.user)
            like.delete()
        
        return redirect("elaborate",id=id)

def add_comment(request,id):
    post = Post.objects.get(id=id)
    comment_text = request.POST.get("comment_content")
    user = User.objects.get(username=request.user)
    comment = Comment.objects.create(post=post,author=user,text=comment_text)
    comment.save()
    return redirect("elaborate",id=id)
    
def del_comment(request,id):
    comment = Comment.objects.get(id=id,author=request.user)
    comment.delete()
    return redirect("elaborate",id=id)

def book_ticket(request,id,price):
    post = Post.objects.get(id=id)
    user = User.objects.get(username=request.user)
    ticket = Ticket.objects.create(event=post,buyer=user,total_price=price)
    return redirect("elaborate",id=id)


@login_required
def profile(request):
    user = request.user

    # Get the user type
    user_type = Usertype.objects.get(user=user).user_type

    # Get the posts the user has liked
    liked_posts = Post.objects.filter(likes__author=user)

    # Get the posts the user has disliked
    disliked_posts = Post.objects.filter(dislikes__author=user)

    # Get the comments made by the user
    commented_posts = Post.objects.filter(comments__author=user)
    # For hosts, get the events they have hosted
    hosted_events = Post.objects.filter(author=user) if user_type == 'host' else None
    booked_posts = Post.objects.filter(ticket__buyer=user)
    for post in booked_posts:
        margin = Ticket.platform_fees/100
        post.adjusted_ticket_fare = (post.Ticket_fare * margin) + post.Ticket_fare
    # Pass the data to the template
    return render(request, 'a/profile.html', {
        'liked_posts': liked_posts,
        'disliked_posts': disliked_posts,
        'commented_posts': commented_posts,
        'hosted_events': hosted_events,
        'user_type': user_type,
        'booked_posts':booked_posts
    })


def generate_ticket(request, ticket_id):
    # Get the ticket based on ticket_id
    ticket = Ticket.objects.get(id=ticket_id)
    post = ticket.event  # The post related to the ticket
    buyer = ticket.buyer  # The user who purchased the ticket
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()
    # Create a canvas to write the PDF
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    # Add ticket information to the PDF
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 80, f"Customer Name: {ticket.buyer.username}")
    p.drawString(100, height - 100, f"Ticket for: {post.title}")
    p.drawString(100, height - 120, f"Event Date: {post.event_date.strftime('%B %d, %Y, %I:%M %p')}")
    p.drawString(100, height - 140, f"Location: {post.location}")
    p.drawString(100, height - 160, f"Ticket Fare: ${post.Ticket_fare}")
    p.drawString(100, height - 180, f"Buyer: {buyer.username}")
    p.drawString(100, height - 200, f"Ticket ID: {ticket.id}")
    # Save the PDF to the buffer
    p.showPage()
    p.save()
    # Move buffer position to the beginning
    buffer.seek(0)
    # Create a downloadable response
    response = HttpResponse(buffer, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.id}.pdf"'
    return response

@login_required
def subscribe(request):
    # Check if the user has a subscription
    s = Subscription.objects.filter(user=request.user)
    if s.exists():
        timeofsub = Subscription.objects.get(user=request.user).end_date
        return render(request,"a/subscribed.html",{"subscription_status":"Already a Subscription!","time":timeofsub})
    else:
        return render(request,"a/subscribed.html",{"subscription_status":"Get Subscription!"})    

from datetime import timedelta
@login_required
def sub(request):
    s = Subscription.objects.create(user=request.user,fees=500,start_date=timezone.now(),end_date=timezone.now()+timedelta(days=30))
    return redirect('subscribe')