from django.shortcuts import render,HttpResponse
from chatbotapp.models import record_sound , recognize_speech
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# @csrf_exempt
# Create your views here.
def index(request):
    return render(request,'chatbotapp/home.html')
def upload_audio(request):
    print("hello")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            audio_data = data.get('audioData')
            # recording = record_sound()
            speech = recognize_speech()
            response_data = {'status': 'success', 'message': speech}
            print(speech)
            return JsonResponse(response_data)
        except Exception as e:
            response_data = {'status': 'error', 'message': str(e)}
            return JsonResponse(response_data, status=500)
