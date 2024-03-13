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
from pydub import AudioSegment
from pydub.playback import play

# Create your views here.
# @csrf_exempt
def index(request):
    return render(request,'chatbotapp/index.html')
      
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



def text_to_numeric(text):
    # Define a mapping dictionary for English number words
    number_mapping = {
        'zero': '0',
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }

    # Split the text into words
    words = text.split()

    # Iterate over the words and replace English number words with their numerical equivalents
    for i in range(len(words)):
        if words[i].lower() in number_mapping:
            words[i] = number_mapping[words[i].lower()]

    # Join the modified words back into a single string
    modified_text = ' '.join(words)

    return modified_text


@csrf_exempt
def talktoOlama(request):
    if request.method=='POST':
        error=""
        try:
            received_data = json.loads(request.body)
            text_data = received_data.get('audio_data')
            text_data = text_to_numeric(text_data)

            olamaReturn = OlamaPreprocess(text_data)
            print(olamaReturn)
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
                    data = f"Hi {response['name']}! , Welcome to Trio-Group ,Your account number is {response['acc_no']}, and You hava Rupees {response['balance']} in your account"
                    tts(data)
                    return JsonResponse({"message": data}, status=200)
                else:
                    tts("User not found")
                    return JsonResponse({"error": "User not found"}, status=404)
            
            elif(api_call=='transferMoney'):
                sender_acc_no = api_body['acc_no1']
                receiver_acc_no = api_body['acc_no2']
                amount = api_body['amount']
                response = transferMoney(sender_acc_no=sender_acc_no,receiver_acc_no=receiver_acc_no,amount=amount)
                tts(response['message'])
                return JsonResponse({"message":response['message']},status = response['status'])
        except Exception as e:
            error = e
            print("the error is ", e)
    tts(error)
    return JsonResponse({"message":error},status =200)

def preprocessText(text):

    try:
        text = text.replace("\n","")
        text = text.replace("\\","")
        start_text = -1
        end_text = -1
        print("the text modified",text)
        temo_list = []
        for i in range(len(text)):
            if text[i]=='{':
                start_text = i
            elif text[i]=='}':
                end_text = i  
                if start_text != -1 and end_text != -1:
                    # text = text[start_text:end_text+1]
                    temo_list.append(text[start_text:end_text+1])
                    print("and here")
                else:
                    text = "Error: No JSON object found in the input."
                start_text = -1
                end_text = -1
        print("No problem till here",temo_list)
        try:
            text = json.loads(temo_list[-1])
            print("rahul here",text)
        except Exception as e:
            text = e ="Error"
    except Exception as e:
        text = "Error"
        print(e)
    return text


def OlamaPreprocess(text):
    api_call=""
    api_body = {}
    
    response = _response(text)
    print("We git the response from olama as",response,"yes")
    response = preprocessText(response)
    print("Preprocessing text",response)
    try:
        if(response=="Error"):
            return response

        if 'get' in response['api_call']:
            print("Trye he")
            try:
                # Assuming 'response' is a dictionary
                for i, (key, value) in enumerate(response.items(), start=1):
                    print("We started", i, key, value, "We ended")
                    api_call = 'getUserDetails'
                    if 'acc' in key:
                        api_body['acc_no'] = value

            except Exception as e:
                api_call = 'Not Valid data'
        
        elif 'trans' in response['api_call']:
            try:
                for i, (key, value) in enumerate(response.items(), start=1):
                    print("We started", i, key, value, "We ended")
                    api_call='transferMoney'
                    if 'sender' in key:
                        api_body['acc_no1']=value
                    if 'rec' in key:
                        api_body['acc_no2'] =value 
                    try:
                        if 'amount' in key and value.isdigit():
                            api_body['amount']= value
                    except Exception as e:
                        print("Error in converting to integer ,but i am making it temporary number")
                        api_body['amount']=50
                
            except Exception as e:
                api_call='Not Valid data'
        else:
            api_call='Not Valid data'
    
    except Exception as e:
        api_call = "Server Side Error"
        
    return {
        "api_call":api_call,
        "api_body":api_body
    }





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
    return {"message":f"{sender.customerName} has transferred {receiver.customerName} Rupees{amount} successfully, Current Balance of {sender.customerName} is {sender.balance}", "status":200}
    



@csrf_exempt
def _response(text, url="http://localhost:11434/api/generate"):
    # data = json.loads(data.body.decode('utf-8'))
    # print(f"I get the data as {data}: {type(data)}")
    # input_text = data['prompt']
    # data['model'] = 'rahul'
    # getIntent = input_text
    # data['prompt']=getIntent
    data = {}
    data['model']='rahul'
    data['stream']=False
    data['prompt']=text
    print(data)
    response = requests.post(url, json=data)
    print(response.text)
    if response.status_code == 200:
        response_text = response.text
        response_lines = response_text.splitlines()
        response_json = json.loads(response_lines[0])['response']
        
    # return JsonResponse({"this":"hello"})
        return response_json
    return response.text
    # else:
    #     return "Error:", response.status_code

def tts(textToSpeak,urlPiper="http://localhost:5000"):
    outputFilename = "output.wav"
    payload = {'text': textToSpeak}
    r = requests.get(urlPiper, params=payload)
    with open(outputFilename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)

    audio = AudioSegment.from_file(outputFilename, format="wav")
    play(audio)
















# def getDetails(request):
#     if request.method == 'GET':
#         print(request.GET)
#         accNo = request.GET.get('acc_no')
#         print("Acc no ",accNo)
#         user = User.objects.filter(customerAccountNo=accNo).first()
#         if user:
#             response = {
#                 "name":user.customerName,
#                 "acc_no":user.customerAccountNo,
#                 "balance":user.balance
#             }
#             return JsonResponse({"auth_code": response}, status=200)
#         else:
#             return JsonResponse({"error": "User not found"}, status=404)
#     else:
#         return JsonResponse({"error": "Method not allowed"}, status=405)
    