from venv import create
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from .utlis import *
import imp
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext

@csrf_exempt
def create_ec2(request):
    print("context in Http request: \n{}".format(request))
    data=json.loads(request.body.decode("utf-8"))
    print("+++++++++++++++++++++++++++++++\ndata_body: {}".format(data))
    try:
        if request.method == 'POST':
            image_id=data["image_id"]
            instance_type=data["instance_type"]
            key_name=data["key_name"]
            group_name=data["group_name"]
            group_description=data["group_description"]
            security_group = setup_security_group(group_name, group_description)
            instance = create_instance(image_id, instance_type, key_name,[group_name])
            return JsonResponse({"message":"Instance successfully created","instance_id":instance.id})
        return JsonResponse({"message":"invalid http request"})
    except Exception as e:
        print("error in views --> create_ec2\n{}".format(e))
        return JsonResponse({"message":"instance creation failed"})

