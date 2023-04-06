from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Prefetch

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, Label, Legend
from bokeh.palettes import magma, Category20, Category10,Category10_3, viridis, plasma, inferno
from math import pi

from .forms import RegisterForm, LoginForm, NewProjectForm, NewClientForm, AddDivisionsForm, AddScopeForm, AddNewDivisionForm, AddItem

from .models import User, Project, Client, Division, DivisionCost, Scope, Item

# Create your views here.

def index(request):
    return render(request, "estimate/index.html")


@login_required
def dashboard(request):
    projects = Project.objects.all()

    bidding = Project.objects.filter(status='bidding').count()
    awarded = Project.objects.filter(status='awarded').count()
    pre = Project.objects.filter(status='pre-construction').count()
    course = Project.objects.filter(status='course of construction').count()


    
    data = {'status': ['Bidding', 'Awarded', 'Pre-construction', 'Construction'],
            'counts': [bidding, awarded, pre, course]}

    # Compute the start and end angles for each wedge of the pie chart
    angles = []
    total_counts = sum(data['counts'])
    for count in data['counts']:
        angle = count / total_counts * 2 * pi
        angles.append(angle)

    start_angles = []
    current_angle = 0
    for angle in angles:
        start_angles.append(current_angle)
        current_angle += angle

    end_angles = []
    current_angle = 0
    for angle in angles:
        current_angle += angle
        end_angles.append(current_angle)

    source = ColumnDataSource(data=dict(
        start_angle=start_angles,
        end_angle=end_angles,
        fill_color=magma(len(data['status'])),
        status=data['status'],
        counts=data['counts']
    ))

    initial_width = 500
    initial_height = 300

    plot = figure(height=initial_height, width=initial_width, toolbar_location=None, tools="hover", tooltips="@status: @counts", x_range=(-0.5, 1.0))

    plot.outline_line_color = 'black'
    plot.outline_line_width = 1

    plot.xaxis.major_tick_line_color = None
    plot.xaxis.minor_tick_line_color = None
    plot.xaxis.major_label_text_font_size = "0pt"
    plot.xgrid.grid_line_color = None

    plot.yaxis.major_tick_line_color = None
    plot.yaxis.minor_tick_line_color = None
    plot.yaxis.major_label_text_font_size = "0pt"
    plot.ygrid.grid_line_color = None

    plot.min_border_bottom = 40

    title = Label(x=-0.45, y=1.75, text="Project Status", 
              text_font_size="15pt", text_font_style="bold")
    plot.add_layout(title)

    plot.wedge(x=0, y=1, radius=0.3, start_angle='start_angle', end_angle='end_angle', line_color='white', fill_color='fill_color', legend_field='status', source=source)


    script, div = components(plot)

    # Donut
    on_going = Project.objects.filter(progress='on-going').count()
    pending = Project.objects.filter(progress='pending for approval').count()
    revise = Project.objects.filter(progress='revise').count()
    approved = Project.objects.filter(progress='approved').count()


    
    data = {'status': ['On-going', 'Pending', 'Revise', 'Approved'],
            'counts': [on_going, pending, revise, approved]}

    angles = []
    total_counts = sum(data['counts'])
    for count in data['counts']:
        angle = count / total_counts * 2 * pi
        angles.append(angle)

    outer_radius = 0.3
    inner_radius = 0.1


    start_angles = []
    current_angle = 0
    for angle in angles:
        start_angles.append(current_angle)
        current_angle += angle

    end_angles = []
    current_angle = 0
    for angle in angles:
        current_angle += angle
        end_angles.append(current_angle)

    source = ColumnDataSource(data=dict(
        start_angle=start_angles,
        end_angle=end_angles,
        fill_color=viridis(4),
        status=data['status'],
        counts=data['counts']
    ))

    initial_width = 500
    initial_height = 300

    plot = figure(height=initial_height, width=initial_width, toolbar_location=None, tools="hover", tooltips="@status: @counts", x_range=(-0.5, 1.0))

    plot.outline_line_color = 'black'
    plot.outline_line_width = 1

    plot.xaxis.major_tick_line_color = None
    plot.xaxis.minor_tick_line_color = None
    plot.xaxis.major_label_text_font_size = "0pt"
    plot.xgrid.grid_line_color = None

    plot.yaxis.major_tick_line_color = None
    plot.yaxis.minor_tick_line_color = None
    plot.yaxis.major_label_text_font_size = "0pt"
    plot.ygrid.grid_line_color = None

    plot.min_border_bottom = 40

    title = Label(x=-0.45, y=1.75, text="Project Progress", 
              text_font_size="15pt", text_font_style="bold")
    plot.add_layout(title)

    plot.annular_wedge(x=0, y=1, inner_radius=inner_radius, outer_radius=outer_radius, start_angle='start_angle', end_angle='end_angle', line_color='white', fill_color='fill_color', legend_field='status', source=source)

    script1, div1 = components(plot)

    return render(request, "estimate/dashboard.html", {
        "projects": projects,
        "script": script,
        "div": div,
        "script1": script1,
        "div1": div1
    })


@login_required
@user_passes_test(lambda user: user.role == 'estimator')
def create_new_project(request):
    if request.method == "POST":
        form = NewProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            client = form.cleaned_data.get("client")
            address = form.cleaned_data.get("address")
            description = form.cleaned_data.get("description")
            status = form.cleaned_data.get("status")
            area = form.cleaned_data.get("area")
            bid_deadline = form.cleaned_data.get("bid_deadline")
            estimator = form.cleaned_data.get("estimator")
            manager = form.cleaned_data.get("manager")
            p = Project(name=name, client=client, address=address, description=description, status=status, area=area, bid_deadline=bid_deadline, estimator=estimator, manager=manager)
            p.save()
            divisions = form.cleaned_data.get("divisions")
            p.divisions.add(*divisions)
            p.save()
            
            for division in p.divisions.all():
                division_cost = DivisionCost(project=p, division=division)
                division_cost.save()
            return HttpResponseRedirect(reverse("dashboard"))
    else:
        form = NewProjectForm()
        form1 = NewClientForm()
    return render(request, "estimate/create_new_project.html", {
        "form": form,
        "form1": form1
    })


@csrf_exempt
@login_required
def add_new_client(request):
    if request.method == 'POST':
        name = request.POST.get("name", "")
        address = request.POST.get("address", "")
        image = request.FILES.get("image", None)

        client = Client(name=name, address=address)

        if image:
            filename = default_storage.save(image.name, ContentFile(image.read()))
            client.image = filename

        client.save()

        return JsonResponse({"message": "Client added successfully."}, status=201)
    

@login_required
def project(request, project_id):
    project = Project.objects.get(pk=project_id)
    divisions = Division.objects.filter(project=project).prefetch_related(
        Prefetch('scopes', queryset=Scope.objects.filter(project=project)),
        Prefetch('division_costs', queryset=DivisionCost.objects.filter(project=project))
    )

    return render(request, "estimate/project.html", {
        "project": project,
        "divisions": divisions
    })


@login_required
def detailed(request, project_id):
    project = Project.objects.get(pk=project_id)
    divisions = project.divisions.all().prefetch_related(
        Prefetch('scopes', queryset=Scope.objects.filter(project=project))
    )

    form = AddDivisionsForm(project=project)
    form1 = AddScopeForm(project=project)
    form2 = AddNewDivisionForm()
    form3 = AddItem(project=project)

    return render(request, "estimate/detailed.html", {
        "project": project,
        "divisions": divisions,
        "form": form,
        "form1": form1,
        "form2": form2,
        "form3": form3
    })


@login_required
def add_divisions(request, project_id):
    project = Project.objects.get(pk=project_id)
    if request.method == "POST":
        form = AddDivisionsForm(project=project, data=request.POST)
        if form.is_valid():
            divisions = form.cleaned_data.get("divisions")
            project.divisions.add(*divisions)
            project.save()

            for division in divisions:
                division_cost = DivisionCost(project=project, division=division)
                division_cost.save()
            return HttpResponseRedirect(reverse("detailed", args=(project_id,)))


@login_required
def remove_division(request, project_id):
    if request.method == "POST":
        project = Project.objects.get(pk=project_id)
        division_id = request.POST["division_id"]
        division = Division.objects.get(pk=division_id)

        division_cost = division.division_costs.get(project=project)
        project.material -= division_cost.material
        project.labor -= division_cost.labor
        project.equipment =- division_cost.equipment
        division_cost.delete()

        project.divisions.remove(division)
        project.save()
        return HttpResponseRedirect(reverse("detailed", args=(project_id,)))
    

@login_required
def add_scope(request, project_id):
    project = Project.objects.get(pk=project_id)
    if request.method == "POST":
        form = AddScopeForm(project=project, data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            qty = form.cleaned_data.get("qty")
            unit = form.cleaned_data.get("unit")
            division = form.cleaned_data.get("divisions")

            scope = Scope(name=name, division=division, project=project, qty=qty, unit=unit)
            scope.save()
            return HttpResponseRedirect(reverse("detailed", args=(project_id,)))
        

@login_required
def add_new_division(request, project_id):
    if request.method == "POST":
        project = Project.objects.get(pk=project_id)
        form = AddNewDivisionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")

            division = Division(name=name)
            division.save()
            division_cost = DivisionCost(project=project, division=division)
            division_cost.save()
            project.divisions.add(division)
            project.save()
            return HttpResponseRedirect(reverse("detailed", args=(project_id,)))


@login_required
def remove_scope(request, project_id):
    if request.method == "POST":
        scope_id = request.POST["scope_id"]
        scope = Scope.objects.get(pk=scope_id)

        project = Project.objects.get(pk=project_id)
        division_cost = scope.division.division_costs.get(project=project)
        division_cost.material -= scope.material
        division_cost.labor -= scope.labor
        division_cost.equipment -= scope.equipment
        division_cost.save()

        project.material -= scope.material
        project.labor -= scope.labor
        project.equipment -= scope.equipment
        project.save()

        scope.delete()
        return HttpResponseRedirect(reverse("detailed", args=(project_id,)))
    

@login_required
def add_item(request, project_id):
    if request.method == "POST":
        project = Project.objects.get(pk=project_id)
        form = AddItem(project=project, data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            qty = form.cleaned_data.get("qty")
            unit = form.cleaned_data.get("unit")
            unit_price = form.cleaned_data.get("unit_price")
            amount = qty * unit_price
            scope = form.cleaned_data.get("scope")
            type = form.cleaned_data.get("type")

            item = Item(name=name, qty=qty, unit=unit, unit_price=unit_price, amount=amount, scope=scope, type=type)
            item.save()

            if item.type.name == "material":
                scope.material += item.amount
                scope.save()
                
                division_cost = scope.division.division_costs.get(project=project)
                division_cost.material += item.amount
                division_cost.save()

                project.material += item.amount
                project.save()
            elif item.type.name == "labor":
                scope.labor += item.amount
                scope.save()
                
                division_cost = scope.division.division_costs.get(project=project)
                division_cost.labor += item.amount
                division_cost.save()

                project.labor += item.amount
                project.save()
            elif item.type.name == "equipment":
                scope.equipment += item.amount
                scope.save()
                
                division_cost = scope.division.division_costs.get(project=project)
                division_cost.equipment += item.amount
                division_cost.save()

                project.equipment += item.amount
                project.save()

            return HttpResponseRedirect(reverse("detailed", args=(project_id,)))
        
@login_required
@csrf_exempt
def remove_item(request, project_id):
    if request.method == "POST":
        project = Project.objects.get(pk=project_id)
        item_id = request.POST["item_id"]
        item = Item.objects.get(pk=item_id)

        if item.type.name == "material":
            scope = item.scope
            scope.material -= item.amount
            scope.save()

            division_cost = scope.division.division_costs.get(project=project)
            division_cost.material -= item.amount
            division_cost.save()

            project.material -= item.amount
            project.save()
        elif item.type.name == "labor":
            scope = item.scope
            scope.labor -= item.amount
            scope.save()

            division_cost = scope.division.division_costs.get(project=project)
            division_cost.labor -= item.amount
            division_cost.save()

            project.labor -= item.amount
            project.save()
        elif item.type.name == "equipment":
            scope = item.scope
            scope.equipment -= item.amount
            scope.save()

            division_cost = scope.division.division_costs.get(project=project)
            division_cost.equipment -= item.amount
            division_cost.save()

            project.equipment-= item.amount
            project.save()

        item.delete()

        return HttpResponseRedirect(reverse("detailed", args=(project_id,)))
    

@login_required
def update_markup(request, project_id):
    if request.method == "POST":
        project = Project.objects.get(pk=project_id)
        ocm = request.POST["ocm"]
        profit = request.POST["profit"]

        project.ocm = ocm
        project.profit = profit
        project.save()

        return HttpResponseRedirect(reverse("project", args=(project_id,)))
        
    

@login_required
def get_scope_items(request, scope_id):
    scope = Scope.objects.get(id=scope_id)
    items = scope.items.all()
    project_id = scope.project.id

    item_list = []
    for item in items:
        item_dict = {
            'id': item.id,
            'name': item.name,
            'quantity': item.qty,
            'unit': item.unit,
            'unit_price': item.unit_price,
            'amount': item.amount,
            'type': item.type.name,
            'project_id': project_id,
            'scope_name': scope.name
        }
        item_list.append(item_dict)

    return JsonResponse(item_list, safe=False)


@login_required
@user_passes_test(lambda user: user.role == 'estimator')
def submit_for_approval(request, project_id):
    if request.method == "POST":
        project = Project.objects.get(pk=project_id)
        project.progress = 'pending for approval'
        project.save()

        return HttpResponseRedirect(reverse("project", args=(project_id,)))


@login_required
@user_passes_test(lambda user: user.role == 'estimator')
def estimator_projects(request):
    projects = Project.objects.filter(estimator=request.user)
    return render(request, "estimate/estimator_projects.html", {
        "projects": projects
    })


@login_required
@user_passes_test(lambda user: user.role == 'manager')
def manager_projects(request):
    projects = Project.objects.filter(manager=request.user)
    return render(request, "estimate/manager_projects.html", {
        "projects": projects
    })


@login_required
@user_passes_test(lambda user: user.role == 'manager')
def reject_project(request, project_id):
    if request.method == "POST":
        project = Project.objects.get(pk=project_id)
        reject_msg = request.POST["reject_msg"]
        project.reject_msg = reject_msg
        project.progress = "revise"
        project.save()

        return HttpResponseRedirect(reverse("project", args=(project_id,)))
    

@login_required
@user_passes_test(lambda user: user.role == 'manager')
def approve_project(request, project_id):
    if request.method == "POST":
        project = Project.objects.get(pk=project_id)
        project.reject_msg = ""
        project.progress = "approved"
        project.save()

        return HttpResponseRedirect(reverse("project", args=(project_id,)))


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            role = form.cleaned_data.get("role")
            
            try:
                user = User.objects.create_user(username, email, password)
                user.role = role
                user.save()
            except IntegrityError:
                form.add_error("username", "Username already taken.")

            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
    else:
        form = RegisterForm()
    return render(request, "estimate/register.html", {
        "form": form
    })
    

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboard"))

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("dashboard"))
            else:
                form.add_error("username", "Invalid username and/or password.")
    else:
        form = LoginForm()
    
    return render(request, "estimate/login.html", {
        "form": form
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

