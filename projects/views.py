from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Project, Tag
from django.http import HttpResponse
from .forms import ProjectForm, reviewform
from django.contrib.auth.decorators import login_required
from .utils import searchprojects, paginateprojects
from django.contrib import messages


def projects(request):
    projects, search_query = searchprojects(request)
    custom_range, projects = paginateprojects(request, projects, 3)
    context = {

        'projects': projects,
        'search_query': search_query,
        'custom_range': custom_range
    }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectobj = Project.objects.get(id=pk)
    form = reviewform()
    if request.method == 'POST':
        form = reviewform(request.POST)
        review = form.save(commit=False)
        review.project = projectobj
        review.owner = request.user.profile
        review.save()
        projectobj.getvotecount

        messages.success(request, 'your review successfully submit')
        return redirect('project', pk=projectobj.id)
    return render(request, 'projects/single-project.html', {'project': projectobj, 'form': form})


@login_required(login_url='login')
def createproject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def updateproject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def deleteproject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'delete-object.html', context)
