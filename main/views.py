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
# import os
import subprocess



def index(request,mac_address=''):
    
    if request.method == 'POST':
        search_data = request.POST.get('search')
        users = User.objects.filter(Q(first_name__contains=search_data) | Q(last_name__contains=search_data))\
            .order_by('-date_joined')
    else:
        users = User.objects.order_by('-date_joined')

    paginator = Paginator(users, 6)
    page = request.GET.get('page', 1)
    page_users = paginator.get_page(page)

    context = {
        'mac_address': mac_address,
        # Add other context variables as needed
    }
    print(mac_address)

    return redirect(request, 'profile.html', {'users': page_users})


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

def get_mac_address():
    try:
        # Use subprocess to execute the osquery command
        command = [
            '/Applications/Vistar.app/Contents/MacOS/osqueryi',
            '--header=false',  # Remove header from the output
            '--csv',           # Output in CSV format
            'SELECT REPLACE(CONCAT(hostname, "-", uuid), "-", "_") FROM system_info;'
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        mac_address = result.stdout.strip()
        return mac_address
    except Exception as e:
        print(f"Failed to get MAC address: {e}")
        return None

# @login_required
def sendMessage(request):
    user_to = request.user.email

    subject="Registeration"

    from_user=settings.EMAIL_HOST_USER
    message_text="Hello this email"

    try:
        send_mail(
            subject,
            message_text,
            from_user,
            [user_to],
            fail_silently=False,
        )

        mac_address = get_mac_address()

        redirect_url = f"/main/index/{mac_address}/"
        url = redirect_url
        return redirect(url)
        # return redirect(url)

        # messages.success(request, 'Email sent successfully!')
    except Exception as e:
        messages.error(request, f'Failed to send email: {e}')
    return redirect(url, mac_address)
