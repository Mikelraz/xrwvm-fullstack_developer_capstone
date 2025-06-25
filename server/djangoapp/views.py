import json
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import analyze_review_sentiments, get_request, post_review


logger = logging.getLogger(__name__)


def get_cars(request):
    """Return JSON list of car models and makes, populating data if empty."""
    count = CarMake.objects.count()
    logger.debug("CarMake count: %d", count)
    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make")
    cars = [
        {"CarModel": cm.name, "CarMake": cm.car_make.name}
        for cm in car_models
    ]
    return JsonResponse({"CarModels": cars})


@csrf_exempt
def login_user(request):
    """Authenticate and log in a user via JSON payload."""
    data = json.loads(request.body)
    username = data.get("userName")
    password = data.get("password")

    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})

    return JsonResponse({"userName": username})


def logout_request(request):
    """Log out the current user."""
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    """Register a new user and log them in."""
    data = json.loads(request.body)
    username = data.get("userName")
    password = data.get("password")
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")

    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"userName": username, "error": "Already Registered"},
        )

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email,
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


def get_dealerships(request, state="All"):
    """Fetch and return dealerships, optionally filtered by state."""
    endpoint = f"/fetchDealers/{state}" if state != "All" else "/fetchDealers"
    dealers = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealers})


def get_dealer_details(request, dealer_id):
    """Fetch and return a single dealer's details."""
    endpoint = f"/fetchDealer/{dealer_id}"
    dealer = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer": dealer})


def get_dealer_reviews(request, dealer_id):
    """Fetch and return dealer reviews with sentiment analysis."""
    reviews = get_request(f"/fetchReviews/dealer/{dealer_id}") or []
    for rev in reviews:
        sentiment = analyze_review_sentiments(rev.get("review", ""))
        rev["sentiment"] = sentiment.get("sentiment") if sentiment else None
    return JsonResponse({"status": 200, "reviews": reviews})


def add_review(request):
    """Post a review if the user is authenticated."""
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

    try:
        data = json.loads(request.body)
        post_review(data)
        return JsonResponse({"status": 200})
    except Exception as err:
        logger.error(
            "Error posting review: %s",
            err,
        )
        return JsonResponse(
            {"status": 401, "message": "Error in posting review"},
        )
