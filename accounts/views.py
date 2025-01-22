from django.shortcuts import render, redirect
from django.http import JsonResponse
from pymongo import MongoClient
import json

# MongoDB connection
client = MongoClient("mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority")
db = client['website_db']
users_collection = db['users']

def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = request.POST.get("username")
        department = request.POST.get("department")
        pass_out_year = request.POST.get("pass_out_year")

        # Check for existing user
        if users_collection.find_one({"email": email}):
            return JsonResponse({"error": "Email already registered!"}, status=400)

        # Save the new user
        users_collection.insert_one({
            "email": email,
            "password": password,  # Use hashed password in production
            "username": username,
            "department": department,
            "pass_out_year": pass_out_year
        })

        return redirect('login')

    return render(request, "signup.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate user
        user = users_collection.find_one({"email": email, "password": password})
        if user:
            request.session['user_id'] = str(user['_id'])
            return redirect('chat_room')  # Placeholder for chat room

        return JsonResponse({"error": "Invalid email or password!"}, status=401)

    return render(request, "login.html")
