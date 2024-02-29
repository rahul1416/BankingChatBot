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

@csrf_exempt
def talktoOlama(request):
    if request.method=='POST':
        received_data = json.loads(request.body)
        text_data = received_data.get('audio_data')
        olamaReturn = OlamaPreprocess(text_data)
        api_call = olamaReturn['api_call']
        api_body = olamaReturn['api_body']
        if(api_call=='getUserDetails'):
            user = User.objects.filter(customerAccountNo=api_body['acc_no']).first()
            if user:
                response = {
                    "name":user.customerName,
                    "acc_no":user.customerAccountNo,
                    "balance":user.balance
                }
                data = f'Hi {response['name']}! , Welcome to Trio-Group ,Your account number is {response['acc_no']}, and You hava Rs{response['balance']} in your account'
                return JsonResponse({"message": data}, status=200)
            else:
                return JsonResponse({"error": "User not found"}, status=404)
        
        elif(api_call=='transferMoney'):
            sender_acc_no = api_body['acc_no1']
            receiver_acc_no = api_body['acc_no2']
            amount = api_body['amount']
            response = transferMoney(sender_acc_no=sender_acc_no,receiver_acc_no=receiver_acc_no,amount=amount)
            return JsonResponse({"message":response['message']},status = response['status'])

    return JsonResponse({"message":"Error"},status =404)




def OlamaPreprocess(text):
    api_call=""
    api_body = {}
    
    if 'transfer' in text:
        api_call='transferMoney'
        api_body['acc_no1']=1
        api_body['acc_no2']=3
        api_body['amount']=100
    else:
        api_call = 'getUserDetails'
        api_body['acc_no']=3
    return {
        "api_call":api_call,
        "api_body":api_body
    }




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
            print("Error",e)
            text = "Failed Error,Try refreshing it/or try after some time"
            print(e)
        response_data = {'status': 'success', 'model': 'rahul','prompt': text}

    
    return JsonResponse(response_data,status=200)



def transferMoney(sender_acc_no,receiver_acc_no,amount):
    # Check if sender and receiver accounts exist
    sender = get_object_or_404(User, customerAccountNo=sender_acc_no)
    receiver = get_object_or_404(User, customerAccountNo=receiver_acc_no)
    
    amount =str(amount)
    # Check if the amount is valid
    if not amount or not amount.isdigit():
        return {"message":"Invalid amount", "status":200}

    # Convert amount to integer
    amount = int(amount)

    # Ensure sender has enough balance
    if sender.balance < amount:
        return {"message":"Insufficient balance", "status":200}

    # Update sender and receiver balances
    sender.balance -= amount
    receiver.balance += amount

    # Save changes to the database
    sender.save()
    receiver.save()
    return {"message":f"{sender.customerName} has transferred {receiver.customerName} Rs{amount} successfully, Current Balance:{sender.balance}", "status":200}
    



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