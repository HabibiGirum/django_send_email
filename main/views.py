from django.http import HttpResponseForbidden, HttpResponse 
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth.decorators import login_required

from .models import Project, Message
from django.contrib import messages
from django.template.loader import render_to_string


from django.core.mail import send_mail
from django.conf import settings



def index(request):
    if request.method == 'POST':
        search_data = request.POST.get('search')
        users = User.objects.filter(Q(first_name__contains=search_data) | Q(last_name__contains=search_data))\
            .order_by('-date_joined')
    else:
        users = User.objects.order_by('-date_joined')

    paginator = Paginator(users, 6)
    page = request.GET.get('page', 1)
    page_users = paginator.get_page(page)

    return render(request, 'profile.html', {'users': page_users})


# def projects(request):
#     if request.method == 'POST':
#         search_data = request.POST.get('search')
#         projects = Project.objects.filter(title__contains=search_data).order_by('-date')
#     else:
#         projects = Project.objects.order_by('-date')

#     paginator = Paginator(projects, 6)
#     page = request.GET.get('page', 1)
#     page_projects = paginator.get_page(page)

#     return render(request, 'projects.html', {'projects': page_projects})


# def singleProject(request, id):
#     project = Project.objects.get(id=id)
#     if request.method == 'POST':
#         project.comment_set.create(
#             author=request.user,
#             text=request.POST.get('message')
#         )
#         return redirect('single-project', project.id)

#     return render(request, 'single-project.html', {'project': project})


# @login_required(login_url='login')
# def inbox(request):
#     messages = Message.objects.filter(user_to=request.user).order_by('-date')
#     unread = messages.filter(is_read=False).count()
#     return render(request, 'inbox.html', {'messages': messages, 'unread': unread})


# @login_required(login_url='login')
# def singleMessage(request, id):
#     message = Message.objects.get(id=id)
#     if message.user_to == request.user:
#         message.is_read = True
#         message.save()
#         return render(request, 'message.html', {'message': message})

#     return HttpResponseForbidden

# @login_required
def sendMessage(request):
    user_to = request.user.email

    subject="Registeration"
    template_path = 'templates/Registeration.html'

    from_user=settings.EMAIL_HOST_USER
    message_htm="Hello this email"

    try:
        # message_html = render_to_string(template_path)

        send_mail(
            subject,
            message_htm,
            from_user,
            [user_to],
            fail_silently=False,
        )
        messages.success(request, 'Email sent successfully!')
    except Exception as e:
        messages.error(request, f'Failed to send email: {e}')
    return redirect('index')
