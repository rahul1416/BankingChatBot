from django.shortcuts import render,HttpResponse
from .record import get_text_from_voice
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from pydub import AudioSegment
import io
from .models import User
import requests

# Create your views here.
# @csrf_exempt
def index(request):
    return render(request,'chatbotapp/home.html')
      
def getLogin(request):
    if request.method == 'GET':
        print(request.GET)
        name = request.GET.get('name')
        accNo = request.GET.get('acc_no')
        print("Acc no ",accNo)
        user = User.objects.filter(customerAccountNo=accNo, customerName__iexact=name).first()
        if user:
            user_auth_code = user.authCode
            return JsonResponse({"auth_code": user_auth_code}, status=200)
        else:
            return JsonResponse({"error": "User not found"}, status=404)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)



def getDetails(request):
    if request.method == 'GET':
        print(request.GET)
        accNo = request.GET.get('acc_no')
        print("Acc no ",accNo)
        user = User.objects.filter(customerAccountNo=accNo).first()
        if user:
            response = {
                "name":user.customerName,
                "acc_no":user.customerAccountNo,
                "balance":user.balance
            }
            return JsonResponse({"auth_code": response}, status=200)
        else:
            return JsonResponse({"error": "User not found"}, status=404)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)





@csrf_exempt
def sendaudio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        print("Post request made")
        audio_blob = request.FILES['audio']
        audio_content = audio_blob.read()
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_content))
        mono_audio=audio_segment.set_channels(1)
        pcm_audio=mono_audio.set_sample_width(2)
        print("converting the data")
        
        # Specify the path where you want to save the WAV file
        wav_file_path = "static/recording.wav"
        
        # Export audio data to WAV format and save to file
        pcm_audio.export(wav_file_path, format="wav")
        
        print("WAV file saved at:", wav_file_path)
        try:
            text = get_text_from_voice()
            print(text)
        except Exception as e:
            text = "Failed Error,Try refreshing it/or try after some time"
            print(e)
        response_data = {'status': 'success', 'model': 'rahul','prompt': text}

    
    return JsonResponse(response_data,status=200)


@csrf_exempt
def transferMoney(request):
    if request.method == 'POST':
        sender_acc_no = request.POST.get('acc_no1')
        receiver_acc_no = request.POST.get('acc_no2')
        amount = request.POST.get('amount')

        # Check if sender and receiver accounts exist
        sender = get_object_or_404(User, customerAccountNo=sender_acc_no)
        receiver = get_object_or_404(User, customerAccountNo=receiver_acc_no)

        # Check if the amount is valid
        if not amount or not amount.isdigit():
            return HttpResponse("Invalid amount", status=400)

        # Convert amount to integer
        amount = int(amount)

        # Ensure sender has enough balance
        if sender.balance < amount:
            return HttpResponse("Insufficient balance", status=400)

        # Update sender and receiver balances
        sender.balance -= amount
        receiver.balance += amount

        # Save changes to the database
        sender.save()
        receiver.save()

        return HttpResponse("Money Transferred")
    else:
        return HttpResponse("Only POST requests are allowed", status=405)

@csrf_exempt
def _response(data, url="http://localhost:11434/api/generate"):
    data = json.loads(data.body.decode('utf-8'))
    print(f"I get the data as {data}: {type(data)}")
    input_text = data['prompt']
    data['model'] = 'rahul'
    getIntent = input_text
    data['prompt']=getIntent
    print(data)
    response = requests.post(url, json=data)
    print(response.text)
    if response.status_code == 200:
        response_text = response.text
        response_lines = response_text.splitlines()
        response_json = json.loads(response_lines[0])['response']
        
    # return JsonResponse({"this":"hello"})
        return JsonResponse({"response":response_json})
    # else:
    #     return "Error:", response.status_code