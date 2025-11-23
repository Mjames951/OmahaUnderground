from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from chat.models import Report, Topic, Root
from chat.chatforms import TopicForm, RootForm

from .models import *
from .forms import *
from .tools.userhandler import ConfirmUser
from .tools.imagehandler import addImage
from .tools import emailhandler

User = get_user_model()

modelsDictionary = {
    "show": Show,
    "band": Band,
    "label": Label,   
    "venue": Venue,     
    "communitylink": CommunityLink,
    "communitysection": CommunitySection,
    "announcement": Announcement,
    'bandlink': BandLink,
    'site': Site,
    'topic': Topic,
    'root': Root,
}

modelforms = {
    "band": BandForm,
    "label": LabelForm,
    "venue": VenueForm,
    "communitylink": CommlinkForm,
    "communitysection": CommsecForm,
    "announcement": AnnouncementForm,
    'bandlink': BandLinkForm,
    'site': SiteForm,
    'topic': TopicForm,
    'root': RootForm,
}

modelAddImage = {
    'band': 'square',
    'label': 'square',
    'venue': 'square',
    'communitylink': 'smaller',
    'announcement': 'smaller',
}

modelNeedApproval = ['band', 'label', 'communitylink', 'show', 'venue']
modelAdminOnly = ['communitysection', 'announcement', 'site', 'topic']

# where to redirect user after model add/edit/delete
def sendUser(modelname, instance):
            match modelname:
                case "band"|'label'|'venue'|'communitylink'|'root':
                    return redirect(instance.get_absolute_url())
                case 'bandlink':
                    return redirect('bandlinks', bandid=instance.band.id)
                case 'topic':
                    return redirect('chat')
            
            if modelname in modelAdminOnly:
                return redirect("superuser")
            return redirect("index")

@login_required
def addModel(request, modelname, parentid=None):
    if not modelname in modelsDictionary: return redirect("index")

    if modelname in modelAdminOnly:
        if not ConfirmUser(request.user): return redirect("index")

    if request.method == "POST":
        try: form = modelforms[modelname](request.POST, request.FILES)
        except: return redirect("index")
        if form.is_valid():
            try:
                if request.FILES['image']:
                    instance = addImage(form, modelAddImage[modelname])
                else:
                    instance = form.save(commit=False)
            except:
                instance = form.save(commit=False)

            if modelname in modelNeedApproval:
                if request.user.is_trusted(): instance.approved = True
                else: 
                    instance.approved = False
                    emailhandler.admin_alert("approval request")

            if parentid:
                match modelname:
                    case 'bandlink':
                        instance.band = Band.objects.get(id=parentid)

            instance.save()
            if modelname == 'band':
                instance.members.add(request.user)
            elif modelname == 'label':
                instance.associates.add(request.user)
            return sendUser(modelname, instance)
            
    else: form = modelforms[modelname]()
    return render(request, "contribute/add/addmodel.html", {
        "form": form,
        "model": modelname,
    })

def editModel(request, modelname, id):
    if not modelname in modelsDictionary: return redirect("index")

    instance = get_object_or_404(modelsDictionary[modelname], id=id)

    if not ConfirmUser(request.user, modelname, instance): return redirect("index")
    
    if request.method == "POST":
        try: form = modelforms[modelname](request.POST, request.FILES, instance=instance)
        except: return redirect("index")

        if form.is_valid():
            try:
                if request.FILES['image']:
                    instance = addImage(form, modelAddImage[modelname], modelInstance=instance)
                    instance.save()
                else:
                    instance = form.save()
            except:
                instance = form.save()
            return sendUser(modelname, instance)
    else:
        try: form = modelforms[modelname](instance=instance)
        except: return redirect("index")
    return render(request, "contribute/edit/editmodel.html",{
        "form": form,
        "model": modelname,
    })

def deleteInstance(request, modelname, id):
    instance = get_object_or_404(modelsDictionary[modelname], id=id)
    if not ConfirmUser(request.user, modelname, instance): return redirect("index")
    try: instance.delete()
    except: return redirect("restrict")
    return sendUser(modelname, instance)

def contribute(request): return render(request, 'planetplum/contribute.html', {})

#main superuser page
def superuser(request):
    if not request.user.is_admin(): return redirect('index')
    shows = Show.objects.filter(approved=False)
    bands = Band.objects.filter(approved=False)
    labels = Label.objects.filter(approved=False)
    commlinks = CommunityLink.objects.filter(approved=False)
    reports = Report.objects.all()
    accounts = User.objects.count()
    venues = Venue.objects.filter(approved=False)
    return render(request, "planetplum/superuser.html", {
        "shows": shows,
        "bands": bands,
        "labels": labels,
        "commlinks": commlinks,
        "reports": reports,
        "accounts": accounts,
        'sites': Site.objects.all(),
        'venues': venues,
    })

def bandlinks(request, bandid):
    band = get_object_or_404(Band, id=bandid)
    if not ConfirmUser(request.user, 'band', band): return redirect("index")
    links = band.links.all()
    return render(request, 'planetplum/bandlinks.html', {
        'band': band,
        'links': links,
    })


@login_required
def addShow(request):
    if request.method == "POST":
        showForm = ShowForm(request.POST, request.FILES)
        venueForm = SubVenueForm(request.POST, prefix='ven')
        if showForm.is_valid():
            print(showForm.cleaned_data)
            show = addImage(showForm, 'smaller') 
            if show:
                if request.user.is_trusted(): show.approved = True
                else: 
                    show.approved = False
                    emailhandler.admin_alert("approval request")
                show.contributor = request.user
                if showForm.cleaned_data['venue'] != Venue.objects.get(name='-- Other Venue --'):
                    show.venue = Venue.objects.get(name=showForm.cleaned_data['venue'])
                    show.save()
                    return redirect(show.get_absolute_url())
                else:
                    if venueForm.is_valid():
                        venueName = venueForm.cleaned_data['name']
                        venueageRange = venueForm.cleaned_data['ageRange']
                        venuedm = venueForm.cleaned_data['dm']
                        venue = Venue(name=venueName, ageRange=venueageRange, dm=venuedm)
                        if not request.user.is_trusted(): 
                            venue.approved = False
                            emailhandler.admin_alert("approval request")
                        venue.save()
                        show.venue = venue
                        show.save()
                        print("IT WORKED")
                        return redirect(show.get_absolute_url())
                    else:
                        print("didn't work")
    #GET method or invalid form
    else: 
        showForm = ShowForm()
        venueForm = SubVenueForm(prefix='ven')
    return render(request, "contribute/add/addshow.html",{
        "form": showForm,
        "venueform": venueForm
    })

def editShow(request, showid):
    try: show = get_object_or_404(Show, id=showid)
    except: return redirect("index")
    if not ConfirmUser(request.user) or not request.user == show.contributor: redirect("index")

    if request.method == "POST":
        showForm = ShowForm(request.POST, request.FILES, instance=show, initial={'venue': show.venue.id})
        venueForm = SubVenueForm(request.POST, prefix='ven')
        if showForm.is_valid():
            try: 
                if request.FILES['image']:
                    show = addImage(showForm, 'smaller', modelInstance=show)
                else:
                    show = showForm.save( commit = False)
            except:
                show = showForm.save( commit = False)

            if showForm.cleaned_data['venue'] != Venue.objects.get(name='-- Other Venue --'):
                show.venue = Venue.objects.get(name=showForm.cleaned_data['venue'])
                show.save()
                return redirect(show.get_absolute_url())
            else:
                if venueForm.is_valid():
                    venueName = venueForm.cleaned_data['name']
                    venueageRange = venueForm.cleaned_data['ageRange']
                    venuedm = venueForm.cleaned_data['dm']
                    venue = Venue(name=venueName, ageRange=venueageRange, dm=venuedm)
                    venue.save()
                    show.venue = venue
                    show.save()
                    return redirect(show.get_absolute_url())
                else:
                    pass
    #GET method or invalid form
    else: 
        showForm = ShowForm(instance=show, initial={'venue': show.venue.id})
        venueForm = SubVenueForm(prefix='ven')
    return render(request, "contribute/edit/editshow.html",{
        "form": showForm,
        "venueform": venueForm,
        "model": "show",
    })

def commSecList(request):
    if not ConfirmUser(request.user): return redirect("index")
    sections = CommunitySection.objects.all()
    return render(request, "contribute/commseclist.html", {
        "sections": sections,
    })

def approveModel(request, modelname, identifier):
    if not ConfirmUser(request.user): return redirect("index")
    model = modelsDictionary[modelname]
    # show instances are found through their ID number,
    #   as other models can be identified through their unique names
    if modelname == 'show': instance = get_object_or_404(model, id=identifier)
    else: instance = get_object_or_404(model, name=identifier)
    instance.approved = True
    instance.save()
    return redirect(instance.get_absolute_url())

def removeMessage(request, reportid):
    if not ConfirmUser(request.user): return redirect("index")
    report = get_object_or_404(Report, id=reportid)
    report.post.delete()
    return redirect("superuser")

def dismissMessage(request, reportid):
    if not ConfirmUser(request.user): return redirect("index")
    report = get_object_or_404(Report, id=reportid)
    report.delete()
    return redirect("superuser")

def restrict(request):
    return render(request, 'contribute/restrict.html', None)



# this whole section below should be compressed down somehow
def userManage(request, usecase, id=None):
    results=None
    title="users"

    match usecase:
        case 'admins':
            if not request.user.is_superuser: return redirect("index")
            active = User.objects.filter(admin=True)
            title="Manage Admins"
            back = reverse('superuser')
        case 'users':
            if not request.user.is_superuser: return redirect("index")
            active = None
            title="Manage Users"
            back = reverse('superuser')
        case 'bandmembers':
            band = get_object_or_404(Band, id=id)
            if not ConfirmUser(request.user, "band", band): return redirect("index")
            title=f"Manage {band.name} Members"
            active = band.members.all()
            back = reverse('bandpage', args = [band.name])
        case 'labelassociates':
            label = get_object_or_404(Label, id=id)
            if not ConfirmUser(request.user, "label", label): return redirect("index")
            title=f"Manage {label.name} Associates"
            active = label.associates.all()
            back = reverse('labelpage', args = [label.name])

    if request.method == "POST":
        form = GeneralSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['Search']
            if usecase == "users":
                active = User.objects.filter(username__icontains=search)
            else: 
                results = User.objects.filter(username__icontains=search).difference(active)
    else: form = GeneralSearchForm()

    return render(request, 'contribute/usermanage.html', {
        "active": active,
        "form": form,
        'results': results,
        "title": title,
        "usecase": usecase,
        "id": id,
        "back": back,
    })

def userManageAddUser(request, usecase, id, username):
    user=get_object_or_404(User, username=username)

    match usecase:
        case 'trust':
            if not ConfirmUser(request.user): return redirect("index")
            user.trusted = True
            user.save()
            return redirect('userprofile', username=user.username)
        case 'admins':
            if not ConfirmUser(request.user): return redirect("index")
            user.admin = True
            user.save()
        case 'bandmembers':
            band = get_object_or_404(Band, id=id)
            if not ConfirmUser(request.user, "band", band): return redirect("index")
            band.members.add(user)
        case 'labelassociates':
            label = get_object_or_404(Label, id=id)
            if not ConfirmUser(request.user, "label", label): return redirect("index")
            label.associates.add(user)


    return redirect("usermanage", usecase, id)

def userManageRemoveUser(request, usecase, username, id=None):
    user=get_object_or_404(User, username=username)

    match usecase:
        case "trust":
            if not ConfirmUser(request.user): return redirect("index")
            user.trusted = False
            user.save()
            return redirect('userprofile', username=user.username)
        case 'admins':
            if not request.user.is_superuser: return redirect("index")
            user.admin = False
            user.save()
        case 'users':
            if not request.user.is_superuser: return redirect("index")
            if user.userprofile.image:
                del(user.userprofile.image.path)
            user.delete()
        case 'bandmembers':
            band = get_object_or_404(Band, id=id)
            if not ConfirmUser(request.user, "band", band): return redirect("index")
            band.members.remove(user)
        case 'labelassociates':
            label = get_object_or_404(Label, id=id)
            if not ConfirmUser(request.user, "label", label): return redirect("index")
            label.associates.remove(user)


    return redirect("usermanage", usecase, id)