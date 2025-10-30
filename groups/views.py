from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from .models import MainGroup, SubGroup, Student, Course, GroupNote, GroupMessage
from .forms import StudentRegistrationForm
import random

MASTER_PASSWORD = getattr(settings, 'MASTER_ADMIN_PASSWORD', 'prestigious')

def home(request):
    classes = MainGroup.objects.all().order_by('-created_at')
    is_admin = request.session.get('is_admin', False)
    return render(request, 'groups/home.html', {'classes': classes, 'is_admin': is_admin})

def admin_unlock(request):
    if request.method == 'POST':
        pwd = request.POST.get('password','')
        if pwd == MASTER_PASSWORD:
            request.session['is_admin'] = True
            messages.success(request, 'Admin unlocked for this browser session.')
            return redirect('groups:home')
        else:
            messages.error(request, 'Incorrect master admin password.')
            return render(request, 'groups/admin_unlock.html', {'error': 'Incorrect password'})
    return render(request, 'groups/admin_unlock.html')

def admin_logout(request):
    request.session.pop('is_admin', None)
    messages.info(request, 'Admin logged out.')
    return redirect('groups:home')

def class_detail(request, pk):
    cls = get_object_or_404(MainGroup, pk=pk)
    subgroups = cls.subgroups.all()
    is_admin = request.session.get('is_admin', False)
    return render(request, 'groups/class_detail.html', {'cls': cls, 'subgroups': subgroups, 'is_admin': is_admin})

def register(request, pk):
    cls = get_object_or_404(MainGroup, pk=pk)
    if request.method == 'POST':
        entered = request.POST.get('join_password','')
        if entered != cls.join_password:
            messages.error(request, 'Incorrect join password.')
            return redirect('groups:register', pk=pk)
        form = StudentRegistrationForm(request.POST)
        form.fields['courses'].queryset = cls.courses.all()
        if form.is_valid():
            subgroup_id = request.POST.get('subgroup')
            subgroup = get_object_or_404(SubGroup, pk=int(subgroup_id))
            if subgroup.members.count() >= cls.max_members:
                messages.error(request, 'Selected subgroup is full.')
                return redirect('groups:register', pk=pk)
            phone = form.cleaned_data['phone']
            if Student.objects.filter(phone=phone).exists():
                messages.error(request, 'Phone already used in the system.')
                return redirect('groups:register', pk=pk)
            student = form.save(commit=False)
            student.subgroup = subgroup
            student.save()
            form.save_m2m()
            messages.success(request, 'Registration successful.')
            return redirect('groups:class_detail', pk=pk)
    else:
        form = StudentRegistrationForm()
        form.fields['courses'].queryset = cls.courses.all()
    subgroups = cls.subgroups.all()
    return render(request, 'groups/register.html', {'cls': cls, 'form': form, 'subgroups': subgroups})

def post_note(request, pk):
    cls = get_object_or_404(MainGroup, pk=pk)
    if request.method == 'POST':
        auth = request.POST.get('auth','')
        title = request.POST.get('title','').strip()
        content = request.POST.get('content','').strip()
        subgroup = get_object_or_404(SubGroup, pk=int(request.POST.get('subgroup')))
        if auth == cls.notes_password or request.session.get('is_admin', False):
            GroupNote.objects.create(subgroup=subgroup, title=title, content=content)
            messages.success(request, 'Note posted.')
        else:
            messages.error(request, 'Auth failed.')
    return redirect('groups:class_detail', pk=pk)

def post_message(request, pk):
    cls = get_object_or_404(MainGroup, pk=pk)
    if request.method == 'POST':
        auth = request.POST.get('auth','')
        content = request.POST.get('content','').strip()
        subgroup = get_object_or_404(SubGroup, pk=int(request.POST.get('subgroup')))
        if auth == cls.notes_password or request.session.get('is_admin', False):
            GroupMessage.objects.create(subgroup=subgroup, content=content)
            messages.success(request, 'Message posted.')
        else:
            messages.error(request, 'Auth failed.')
    return redirect('groups:class_detail', pk=pk)

@transaction.atomic
def select_leader(request, pk, sg_pk):
    cls = get_object_or_404(MainGroup, pk=pk)
    subgroup = get_object_or_404(SubGroup, pk=sg_pk, main_group=cls)
    if subgroup.members.count() < cls.max_members:
        messages.error(request, 'Group not full yet.')
        return redirect('groups:class_detail', pk=pk)
    # auth
    if not request.session.get('is_admin', False):
        auth = request.POST.get('auth','') or request.GET.get('auth','')
        if auth != cls.notes_password and (not cls.delegate_phone or auth != cls.delegate_phone):
            messages.error(request, 'Not authorized to select leader.')
            return redirect('groups:class_detail', pk=pk)
    members = list(subgroup.members.all())
    if not members:
        messages.error(request, 'No members.')
        return redirect('groups:class_detail', pk=pk)
    leader = random.choice(members)
    subgroup.leader = leader
    subgroup.save()
    messages.success(request, f'Leader selected: {leader.name1} {leader.name2}')
    return redirect('groups:class_detail', pk=pk)

def confirm_reset(request):
    is_admin = request.session.get('is_admin', False)
    if request.method == 'POST':
        pwd = request.POST.get('master_password','')
        if pwd == MASTER_PASSWORD:
            MainGroup.objects.all().delete()
            messages.success(request, 'System reset: all classes removed.')
            return redirect('groups:home')
        else:
            messages.error(request, 'Incorrect master password.')
            return redirect('groups:confirm_reset')
    return render(request, 'groups/confirm_reset.html', {'is_admin': is_admin})
