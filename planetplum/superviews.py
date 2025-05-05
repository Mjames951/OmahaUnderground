from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from chat.models import Report
from .tools.imagehandler import addImage
from .models import *
from .forms import *
from .tools.userhandler import ConfirmUser
from django.contrib.auth import get_user_model

User = get_user_model()

def contribute(request):
    return render(request, 'planetplum/contribute.html', {

    })

#main superuser page
def superuser(request):
    if not request.user.is_superuser or not request.user.is_admin: return redirect('index')
    shows = Show.objects.filter(approved=False)
    bands = Band.objects.filter(approved=False)
    labels = Label.objects.filter(approved=False)
    commlinks = CommunityLink.objects.filter(approved=False)
    reports = Report.objects.all()
    return render(request, "planetplum/superuser.html", {
        "shows": shows,
        "bands": bands,
        "labels": labels,
        "commlinks": commlinks,
        "reports": reports,
    })


#replace this eventually with @user_passes_test(our defined function, redirect_field_name)
#have the test check if the user is super, or owner of post/is labelmate or whatever

@login_required
def addShow(request):
    if request.method == "POST":
        showForm = ShowForm(request.POST, request.FILES)
        if showForm.is_valid():
            show = addImage(showForm, 'show') 
            if request.user.is_superuser or request.user.is_admin: show.approved = True
            show = show.save(commit=False)
            show.contributor = request.user
            show.save()
            return redirect("showpage", showid = show.id)
    #GET method or invalid form
    else: showForm = ShowForm()
    return render(request, "contribute/add/addshow.html",{
        "form": showForm,
    })

def editShow(request, showid):
    try: show = get_object_or_404(Show, id=showid)
    except: return redirect("index")
    if not ConfirmUser(request.user) or not request.user == show.contributor: redirect("index")
    if request.method == "POST":
        showForm = ShowForm(request.POST, request.FILES, instance=show)
        if showForm.is_valid():
            if showForm.cleaned_data['image']:
                show = addImage(showForm, 'show', modelInstance=show)
                show.save()
            else:
                show = showForm.save()
            print(show.pwyc)
            print(showForm.cleaned_data)
            return redirect("showpage", showid=showid)
    #GET method or invalid form
    else: showForm = ShowForm(instance=show)
    return render(request, "contribute/edit/editshow.html",{
        "form": showForm,
        "model": "show",
    })

@login_required
def addBand(request):
    if request.method == "POST":
        bandForm = BandForm(request.POST, request.FILES)
        if bandForm.is_valid():
            band = addImage(bandForm, 'band')
            if request.user.is_superuser or request.user.is_admin: band.approved = True
            band.save()
            if band:
                return redirect("bandpage", bandname=band.name)
    #GET method or invalid form
    else: bandForm = BandForm()
    return render(request, "contribute/add/addband.html",{
        "form": bandForm,
    })


def editBand(request, bandname):
    try: band = get_object_or_404(Band, name=bandname)
    except: return redirect("index")
    if not ConfirmUser(request.user, "band", band): return redirect("index")
    if request.method == "POST":
        bandForm = BandForm(request.POST, request.FILES, instance=band)
        if bandForm.is_valid():
            if bandForm.cleaned_data['image']:
                band = addImage(bandForm, 'band', modelInstance=band)
                band.save()
            else:
                bandForm.save()
            return redirect("bandpage", bandname=bandname)
    #GET method or invalid form
    else: bandForm = BandForm(instance=band)
    return render(request, "contribute/edit/editband.html",{
        "form": bandForm,
        "model": "band",
    })

@login_required
def addLabel(request):
    if request.method == "POST":
        labelForm = LabelForm(request.POST, request.FILES)
        if labelForm.is_valid():
            if not labelForm.cleaned_data['image']:
                label = labelForm.save(commit=False)
            else: label = addImage(labelForm, 'band') #same size as band pfp 
            if request.user.is_superuser or request.user.is_admin: label.approved = True
            label.save()
            return redirect("labelpage", labelname=label.name)
    #get method or invalid form
    else: labelForm = LabelForm()
    return render(request, "contribute/add/addlabel.html",{
        "form": labelForm,
    })

def editLabel(request, labelname):
    try: label = get_object_or_404(Label, name=labelname)
    except: return redirect("index")
    if not ConfirmUser(request.user, "label", label): return redirect("index")
    if request.method == "POST":
        labelForm = LabelForm(request.POST, request.FILES, instance=label)
        if labelForm.is_valid():
            if labelForm.cleaned_data['image']:
                label = addImage(labelForm, 'band', modelInstance=label)
                label.save()
            else:
                labelForm.save()
            return redirect("labelpage", labelname=labelname)
    #GET method or invalid form
    else: labelForm = LabelForm(instance=label)
    return render(request, "contribute/edit/editlabel.html",{
        "form": labelForm,
        "model": "label",
    })
    
@login_required
def addVenue(request):
    if request.method == "POST":
        venueForm = VenueForm(request.POST, request.FILES)
        if venueForm.is_valid():
            if not venueForm.cleaned_data['image']:
                venue = venueForm.save(commit=False)
            else: venue = addImage(venueForm, 'band') #same size as bandpfp
            venue.save()
            return redirect("venuepage", venuename=venue.name)
    #GET method or invalid form
    else: venueForm = VenueForm()
    return render(request, "contribute/add/addvenue.html",{
        "form": venueForm
    })

def editVenue(request, venuename):
    try: venue = get_object_or_404(Venue, name=venuename)
    except: return redirect("index")
    if not ConfirmUser(request.user): return redirect("index")
    if request.method == "POST":
        venueForm = VenueForm(request.POST, request.FILES, instance=venue)
        if venueForm.is_valid():
            if venueForm.cleaned_data['image']:
                venue = addImage(venueForm, 'band', modelInstance=venue)
                venue.save()
            else:
                venueForm.save()
            return redirect("venuepage", venuename=venuename)
    #GET method or invalid form
    else: venueForm = VenueForm(instance=venue)
    return render(request, "contribute/edit/editvenue.html",{
        "form": venueForm,
        "model": "venue",
    })

def addAnnouncement(request):
    if not ConfirmUser(request.user): return redirect("index")
    if request.method == "POST":
        announcementForm = AnnouncementForm(request.POST, request.FILES)
        if announcementForm.is_valid():
            if not announcementForm.cleaned_data['image']:
                announcement = announcementForm.save()
            else: 
                announcement = addImage(announcementForm, 'show')
                announcement.save()
            return redirect("index")
    else: announcementForm = AnnouncementForm()
    return render(request, "contribute/add/addannouncement.html",{
        "form": announcementForm,
    })

def editAnnouncement(request, announcementid):
    if not ConfirmUser(request.user): return redirect("index")
    try: announcement = get_object_or_404(Announcement, id=announcementid)
    except: return redirect("index")
    if request.method == 'POST':
        announcementForm = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if announcementForm.is_valid():
            if announcementForm.cleaned_data['image']:
                announcement = addImage(announcementForm, 'show', modelInstance=announcement)
                announcement.save()
            else:
                announcementForm.save()
            return redirect("index")
    else: announcementForm = AnnouncementForm(instance=announcement)
    return render(request, "contribute/edit/editannouncement.html", {
        "form": announcementForm,
        "model": "announcement",
    })

@login_required
def addCommlink(request):
    if request.method == "POST":
        commlinkForm = CommlinkForm(request.POST, request.FILES)
        if commlinkForm.is_valid():
            if not commlinkForm.cleaned_data['image']:
                commlink = commlinkForm.save(commit=False)
            else: commlink = addImage(commlinkForm, 'show')
            if request.user.is_superuser or request.user.is_admin: commlink.approved = True
            commlink.save()
            return redirect("community")
    else: commlinkForm = CommlinkForm()
    return render(request, "contribute/add/addcommlink.html",{
        "form": commlinkForm,
    })

def editCommLink(request, commlinkid):
    if not ConfirmUser(request.user): return redirect("index")
    try: commlink = get_object_or_404(CommunityLink, id=commlinkid)
    except: return redirect("index")
    if request.method == "POST":
        commlinkForm = CommlinkForm(request.POST, request.FILES, instance=commlink)
        if commlinkForm.is_valid():
            if commlinkForm.cleaned_data['image']:
                commlink = addImage(commlinkForm, 'show', modelInstance=commlink)
                commlink.save()
            else:
                commlink.save()
            return redirect("community")
    else: commlinkForm = CommlinkForm(instance = commlink)
    return render(request, "contribute/edit/editcommlink.html", {
        "form": commlinkForm,
        "model": "communitylink",
    })

def commSecList(request):
    if not ConfirmUser(request.user): return redirect("index")
    sections = CommunitySection.objects.all()
    return render(request, "contribute/commseclist.html", {
        "sections": sections,
    })



def addCommSec(request):
    if not ConfirmUser(request.user): return redirect("index")
    if request.method == "POST":
        commsecForm = CommsecForm(request.POST, request.FILES)
        if commsecForm.is_valid():
            commsec = commsecForm.save()
            return redirect("superuser")
    else: commsecForm = CommsecForm()
    return render(request, "contribute/add/addcommlink.html",{
        "form": commsecForm,
    })

def editCommSec(request, sectionid):
    if not ConfirmUser(request.user): return redirect("index")
    try: section = get_object_or_404(CommunitySection, id=sectionid)
    except: return redirect("index")
    if request.method == "POST":
        commsecForm = CommsecForm(request.POST, request.FILES, instance=section)
        if commsecForm.is_valid():
            commsecForm.save()
        return redirect("community")
    else:
        commsecForm = CommsecForm(instance=section)
    return render(request, "contribute/edit/editcommlink.html", {
        "form": commsecForm,
        "model": "communitysection",
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

moptions = {
    "announcement": Announcement,
    "band": Band,
    "communitylink": CommunityLink,
    "label": Label,
    "show": Show,
    "venue": Venue,
    "communitysection": CommunitySection,
}
def deleteInstance(request, model, id):
    if not ConfirmUser(request.user): return redirect("index")
    model = moptions[model]
    try: instance = get_object_or_404(model, id=id)
    except: return redirect("superuser")
    try: instance.delete()
    except: return redirect("restrict")
    return redirect("superuser")

def restrict(request):
    return render(request, 'contribute/restrict.html', None)


def userManage(request, usecase, id=None):
    results=None
    overlord=False
    title="users"

    match usecase:
        case 'admins':
            if not request.user.is_superuser: return redirect("index")
            active = User.objects.filter(admin=True)
            overlord=True
            title="Manage Admins"
        case 'bandmembers':
            band = Band.objects.filter(id=id)
            overlord=True
            title=f"Manage {band.name} Members"

    if request.method == "POST":
        form = GeneralSearchForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            search = form.cleaned_data['Search']
            results = User.objects.filter(username__icontains=search)
            print(results)
    else: form = GeneralSearchForm()


    return render(request, 'contribute/usermanage.html', {
        "active": None,
        "form": form,
        'results': results,
        "overlord": overlord,
        "title": title,
    })