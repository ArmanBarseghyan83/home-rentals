from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from .forms import ListingForm, FindForm
from django.views import View
from django.views.decorators.cache import cache_control

from .models import User, Listing, TourRequest, Property

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    try:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        home_types = Property.objects.all()
        header = ''
        if not request.session.get('data'):
            request.session['data'] = {'search': '','bed': '', 'bath': '', 'min': '', 'max': '', 'house': '', 'condo': '',
                'townhouse': '', 'listing_id': '', 'min_year_built': '', 'max_year_built': ''}
        if request.session.get('data')['listing_id']:
            listings = Listing.objects.filter(id__in=request.session['data']['listing_id'])
            header = "Results for your search!"
        elif request.session.get('data')['listing_id'] == []:
            listings = {} 
            header = "Sorry no results found!"
        else:  
            listings = Listing.objects.all()
            header = "All Homes" 
        form = FindForm()
        filter_data = request.session.get('data')
        is_house = request.session.get('data')['house']
        is_condo = request.session.get('data')['condo']
        is_townhouse = request.session.get('data')['townhouse']
        return render(request, "my_app/index.html", {
            "listings": reversed(listings),
            "form": form,
            "home_types": home_types,
            "header": header,
            "filter_data": filter_data,
            "is_house": is_house,
            "is_condo": is_condo,
            "is_townhouse": is_townhouse,
        })
    except: 
        return render(request, "my_app/index.html", {"header": "Something went wrong!"})
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def listing_details(request, listing_id):
    try:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        if request.method == "POST":
            listing = Listing.objects.get(id=listing_id)
            recipient = listing.owner
            request = TourRequest(listing=listing,sender=request.user, subject=request.POST['subject'], body=request.POST['body'], date=request.POST['date'])
            request.save()
            request.recipients.add(recipient)
            return HttpResponseRedirect(reverse("listing-details", args=(listing_id, )))
    
        listing = Listing.objects.get(id=listing_id)
        tour_requests = TourRequest.objects.filter(recipients=request.user, listing=listing).order_by('date')
        is_request_sent = [i for i in listing.tour_requests.all() if request.user == i.sender] 
        return render(request, "my_app/listing-details.html", {
            "listing": listing,
            "tour_requests": tour_requests,
            "is_request_sent": is_request_sent
        })
    except:
        return render(request, "my_app/listing-details.html", {
            "message": "Sorry could not fetch data!"
        })


class Saved(View):
    def get(self, request):
        try:
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse("login"))
            listings = Listing.objects.filter(saved=request.user)
            form = FindForm()
            return render(request, "my_app/index.html", {
                "listings": reversed(listings),
                "form": form,
                "header": "Saved"
            })
        except:
            return render(request, "my_app/index.html", {"header": "Something went wrong!"})


class UserListing(View):
    def get(self, request):
        try:
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse("login"))
            listings = Listing.objects.filter(owner=request.user)
            form = FindForm()
            return render(request, "my_app/index.html", {
                "listings": listings,
                "form": form,
                "header": "My Listings"
            })
        except:
            return render(request, "my_app/index.html", {"header": "Something went wrong!"})
  
class Find(View):
    def post(self, request):
        if request.session.get('data')['listing_id']:
            listings = Listing.objects.filter(id__in=request.session['data']['listing_id'])
        listings = Listing.objects.filter(address__contains=request.POST['find_input'])
        listings_id = [i.id for i in listings]
        request.session['data'] = {'search': request.POST['find_input'],'bed': '', 'bath': '', 'min': '',
             'max': '', 'house': '', 'condo': '','townhouse': '', 'min_year_built': '', 'max_year_built': '', 'listing_id': listings_id}
        return HttpResponseRedirect(reverse("index"))


class CreateListing(View):
    def get(self, request):
        form = ListingForm()
        return render(request, "my_app/create-listing.html", {
            "form": form
        })
    
    def post(self, request):
        try:
            form = ListingForm(request.POST, request.FILES)
            if form.is_valid():
                listing = form.save(commit=False)
                listing.owner = request.user
                listing.save()
            return HttpResponseRedirect(reverse("index"))
        except:
            form = ListingForm()
            return render(request, "my_app/create-listing.html", {
                "form": form, 
                "message": "Please correct errors"
            })


def reset(request):
    request.session['data'] = ''
    return HttpResponseRedirect(reverse("index"))


def save(request, listing_id):
    if  Listing.objects.filter(id=listing_id, saved=request.user):
        Listing.objects.get(id=listing_id).saved.remove(request.user)
        return JsonResponse({"message": "Unsaved successfully."}, status=201)
    else:
        Listing.objects.get(id=listing_id).saved.add(request.user)   
        return JsonResponse({"message": "Saved successfully."}, status=201)


def requests(request):
    try:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        requests = TourRequest.objects.filter(recipients=request.user).order_by('date')
        return render(request, "my_app/requests.html", {
            "requests": requests 
        })
    except:
        return render(request, "my_app/requests.html", {
            "message": "Could not fetch data!" 
        })

    
def filter(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    listings =Listing.objects.all()

    if request.session.get('data')['search']:
        listings = Listing.objects.filter(address__contains=request.session.get('data')['search'])
        search = request.session.get('data')['search']
    else:    
        search = ''

    if request.POST['bed']:
        listings = listings.filter(bed=request.POST['bed'])
    if request.POST['bath']:
        listings = listings.filter(bed=request.POST['bath'])
    if request.POST['min']:
        listings = listings.filter(price__gt=request.POST['min']) 
    if request.POST['max']:
        listings = listings.filter(price__lt=request.POST['max'])
    if request.POST.get('min_year_built'):
        listings = listings.filter(year_built__gte=request.POST['min_year_built'])   
    if request.POST.get('max_year_built'):
        listings = listings.filter(year_built__lte=request.POST['max_year_built'])     
            
    if  request.POST.get('house', False) or request.POST.get('condo', False) or request.POST.get('townhouse', False): 
        homes = []    
        if request.POST.get('house', False):
            house = Property.objects.get(home_type_name=request.POST.get('house', False))
            homes.append(house) 
        if request.POST.get('condo', False):
            house = Property.objects.get(home_type_name=request.POST.get('condo', False))
            homes.append(house)
        if request.POST.get('townhouse', False):
            house = Property.objects.get(home_type_name=request.POST.get('townhouse', False))
            homes.append(house)  
        listings = listings.filter(home_type__in=homes) 

    listings_id = [i.id for i in listings]         
    
    request.session['data'] = {'search': search, 'min_year_built': request.POST.get('min_year_built'),
        'bed': request.POST.get('bed'), 'bath': request.POST.get('bath'), 'max_year_built': request.POST.get('max_year_built'),
        'min': request.POST.get('min'), 'max': request.POST.get('max'), 'listing_id': listings_id,
        'house': request.POST.get('house', False), 'condo': request.POST.get('condo', False),
        'townhouse': request.POST.get('townhouse', False)}
    return HttpResponseRedirect(reverse("index"))
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "my_app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "my_app/login.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "my_app/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "my_app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "my_app/register.html")