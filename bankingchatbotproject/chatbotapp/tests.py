from django.test import TestCase


# Create your tests here.
def _response(text, url="http://localhost:11434/api/generate"):
    data = json.loads(data.body.decode('utf-8'))
    print(f"I get the data as {data}: {type(data)}")
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
        return JsonResponse({"response":response_json})
    # else:
    #     return "Error:", response.status_code
    _response(text='What is my account balance')