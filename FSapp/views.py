from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pickle
import random

# Load your models
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
responses_dict = pickle.load(open("responses.pkl", "rb"))

def home(request):
    return render(request, "foodstuff.html")  # This will load the chatbot interface

@csrf_exempt
def get_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        query = data.get("message", "")
        if not query:
            return JsonResponse({"response": "Please say something."})
        X_input = vectorizer.transform([query])
        predicted_tag = model.predict(X_input)[0]
        response = random.choice(responses_dict[predicted_tag])
        return JsonResponse({"response": response})
    return JsonResponse({"response": "Invalid request method."})
