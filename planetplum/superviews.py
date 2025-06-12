from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from chat.models import Report
from .tools.imagehandler import addImage
from .models import *
from .forms import *
from .tools.userhandler import ConfirmUser
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

User = get_user_model()

moptions = {
    "show": Show,
    "band": Band,
    "label": Label,   
    "venue": Venue,     
    "communitylink": CommunityLink,
    "communitysection": CommunitySection,
    "announcement": Announcement,
    'bandlink': BandLink,
    'site': Site,
}

mforms = {
    "band": BandForm,
    "label": LabelForm,
    "venue": VenueForm,
    "communitylink": CommlinkForm,
    "communitysection": CommsecForm,
    "announcement": AnnouncementForm,
    'bandlink': BandLinkForm,
    'site': SiteForm,
}

modelAddImage = {
    'band': 'square',
    'label': 'square',
    'venue': 'square',
    'communitylink': 'smaller',
    'announcement': 'smaller',
}

modelNeedApproval = ['band', 'label', 'communitylink', 'show',]
modelAdminOnly = ['communitysection', 'announcement', 'site']

def sendUser(modelname, model):
    #specific where to send user
            match modelname:
                case "band":
                    return redirect("bandpage", bandname=model.name)
                case "label":
                    return redirect("labelpage", labelname=model.name)
                case "venue":
                    return redirect("venuepage", venuename=model.name)
                case "communitylink":
                    return redirect("community")
                case 'bandlink':
                    return redirect('bandlinks', bandid=model.band.id)
            
            if modelname in modelAdminOnly:
                return redirect("superuser")
            return redirect("index")

@login_required
def addModel(request, modelname, parentid=None):
    if not modelname in moptions: return redirect("index")

    if modelname in modelAdminOnly:
        if not ConfirmUser(request.user): return redirect("index")

    if request.method == "POST":
        try: form = mforms[modelname](request.POST, request.FILES)
        except: return redirect("index")
        if form.is_valid():
            try:
                if request.FILES['image']:
                    model = addImage(form, modelAddImage[modelname])
                else:
                    model = form.save(commit=False)
            except:
                model = form.save(commit=False)

            if modelname in modelNeedApproval:
                if request.user.is_trusted(): model.approved = True

            if parentid:
                match modelname:
                    case 'bandlink':
                        model.band = Band.objects.get(id=parentid)

            model.save()
            if modelname == 'band':
                model.members.add(request.user)
            elif modelname == 'label':
                model.associates.add(request.user)
            return sendUser(modelname, model)
            
    else: form = mforms[modelname]()
    return render(request, "contribute/add/addmodel.html", {
        "form": form,
        "model": modelname,
    })

def editModel(request, modelname, id):
    try: model = moptions[modelname]
    except: return redirect("index")

    model = get_object_or_404(model, id=id)

    if not ConfirmUser(request.user, modelname, model):
        return redirect("index")
    
    if request.method == "POST":
        try: form = mforms[modelname](request.POST, request.FILES, instance=model)
        except: return redirect("index")

        if form.is_valid():
            try:
                if request.FILES['image']:
                    model = addImage(form, modelAddImage[modelname], modelInstance=model)
                    model.save()
                else:
                    model = form.save()
            except:
                model = form.save()
            return sendUser(modelname, model)
    else:
        try: form = mforms[modelname](instance=model)
        except: return redirect("index")
    return render(request, "contribute/edit/editmodel.html",{
        "form": form,
        "model": modelname,
    })

def deleteInstance(request, model, id):
    print("DELETING THE THING")
    modelname = model
    model = moptions[model]
    instance = get_object_or_404(model, id=id)
    if not ConfirmUser(request.user, modelname, instance): return redirect("index")
    try: instance.delete()
    except: return redirect("restrict")
    return redirect("index")

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
    return render(request, "planetplum/superuser.html", {
        "shows": shows,
        "bands": bands,
        "labels": labels,
        "commlinks": commlinks,
        "reports": reports,
        "accounts": accounts,
        'sites': Site.objects.all(),
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
                else: show.approved = False
                show.contributor = request.user
                if showForm.cleaned_data['venue'] != Venue.objects.get(name='-- Other Venue --'):
                    show.venue = Venue.objects.get(name=showForm.cleaned_data['venue'])
                    show.save()
                    return redirect("showpage", showid = show.id)
                else:
                    if venueForm.is_valid():
                        venueName = venueForm.cleaned_data['name']
                        venueageRange = venueForm.cleaned_data['ageRange']
                        venuedm = venueForm.cleaned_data['dm']
                        venue = Venue(name=venueName, ageRange=venueageRange, dm=venuedm)
                        venue.save()
                        show.venue = venue
                        show.save()
                        print("IT WORKED")
                        return redirect("showpage", showid = show.id)
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
                    show = addImage(showForm, 'show', modelInstance=show)
                else:
                    show = showForm.save( commit = False)
            except:
                show = showForm.save( commit = False)

            if showForm.cleaned_data['venue'] != Venue.objects.get(name='-- Other Venue --'):
                show.venue = Venue.objects.get(name=showForm.cleaned_data['venue'])
                show.save()
                return redirect("showpage", showid = show.id)
            else:
                if venueForm.is_valid():
                    venueName = venueForm.cleaned_data['name']
                    venueageRange = venueForm.cleaned_data['ageRange']
                    venuedm = venueForm.cleaned_data['dm']
                    venue = Venue(name=venueName, ageRange=venueageRange, dm=venuedm)
                    venue.save()
                    show.venue = venue
                    show.save()
                    return redirect("showpage", showid = show.id)
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

def approveShow(request, showid):
    if not ConfirmUser(request.user): return redirect("index")
    try: show = get_object_or_404(Show, id=showid)
    except: return redirect("index")
    show.approved = True
    show.save()
    return redirect("showpage", showid)

def approveBand(request, bandname):
    if not ConfirmUser(request.user): return redirect("index")
    try: band = get_object_or_404(Band, name=bandname)
    except: return redirect("index")
    band.approved = True
    band.save()
    return redirect("bandpage", bandname)
    
def approveLabel(request, labelname):
    if not ConfirmUser(request.user): return redirect("index")
    try: label = get_object_or_404(Label, name=labelname)
    except: return redirect("index")
    label.approved = True
    label.save()
    return redirect("labelpage", labelname)

def removeMessage(request, reportid):
    if not ConfirmUser(request.user): return redirect("index")
    try: report = get_object_or_404(Report, id=reportid)
    except: return redirect("superuser")
    report.post.delete()
    return redirect("superuser")

def dismissMessage(request, reportid):
    if not ConfirmUser(request.user): return redirect("index")
    try: report = get_object_or_404(Report, id=reportid)
    except: return redirect("superuser")
    report.delete()
    return redirect("superuser")

def restrict(request):
    return render(request, 'contribute/restrict.html', None)


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
            try: band = get_object_or_404(Band, id=id)
            except: return redirect("index")
            if not ConfirmUser(request.user, "band", band): return redirect("index")
            title=f"Manage {band.name} Members"
            active = band.members.all()
            back = reverse('bandpage', args = [band.name])
        case 'labelassociates':
            try: label = get_object_or_404(Label, id=id)
            except: return redirect("index")
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
    try: user=get_object_or_404(User, username=username)
    except: return redirect("index")

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
            try: band = get_object_or_404(Band, id=id)
            except: return redirect("index")
            if not ConfirmUser(request.user, "band", band): return redirect("index")
            band.members.add(user)
        case 'labelassociates':
            try: label = get_object_or_404(Label, id=id)
            except: return redirect("index")
            if not ConfirmUser(request.user, "label", label): return redirect("index")
            label.associates.add(user)


    return redirect("usermanage", usecase, id)

def userManageRemoveUser(request, usecase, username, id=None):
    try: user=get_object_or_404(User, username=username)
    except: return redirect("index")

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
            try: band = get_object_or_404(Band, id=id)
            except: return redirect("index")
            if not ConfirmUser(request.user, "band", band): return redirect("index")
            band.members.remove(user)
        case 'labelassociates':
            try: label = get_object_or_404(Label, id=id)
            except: return redirect("index")
            if not ConfirmUser(request.user, "label", label): return redirect("index")
            label.associates.remove(user)


    return redirect("usermanage", usecase, id)