from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

import json

from centralauth_provider import *

def validate_service(service):
    matching_services = [s[0] for s in CENTRALAUTH_SERVICES if s[0] == service]
    return len(matching_services) == 1

def get_service_attributes(service):
    matching_services = [s[1] for s in CENTRALAUTH_SERVICES if s[0] == service]
    if len(matching_services) == 1:
        return matching_services[0]
    else:
        return None

def render_dict_to_response(data_dict):
    # Return response
    return HttpResponse(content=json.dumps("<body>%s</body>" %(data_dict,)))

def authenticate(request):
    #TODO: Add check to see if request from internal IP

    # Gather the GET data from request
    session_key = request.GET.get('session_key', None)
    service = request.GET.get('service', None)

    data_dict = dict()

    # Check if all required GET data is available
    if all((service, session_key)) is False:
        data_dict['status'] = 'Incorrect request'

    # Check if the service is allowed to request an authentication
    elif validate_service(service) is False:
        data_dict['status'] = 'Invalid service'
        pass

    else:
        # Get session key user
        usernames = User.objects.filter(sessions__key=session_key).values_list('username')
        if len(usernames) == 1:
            data_dict['username'] = usernames[0][0]
            data_dict['status'] = 'Success'
        else:
            data_dict['status'] = 'Invalid Session Key'

    # Return response
    return render_dict_to_response(data_dict)

def get_attributes(request):
    #TODO
    # Gather the GET data from request
    session_key = request.GET.get('session_key', None)
    service = request.GET.get('service', None)

    data_dict = dict()

    # Check if all required GET data is available
    if all((service, session_key)) is False:
        data_dict['status'] = 'Incorrect request'
        return render_dict_to_response(data_dict)

    # Check if the service is allowed to request an authentication
    elif validate_service(service) is False:
        data_dict['status'] = 'Invalid service'
        return render_dict_to_response(data_dict)


    # Get list of attributes that should be provided
    service_attributes = get_service_attributes(service)

    # Get user data from database
    try:
        user = User.objects.get(sessions__key=session_key)
    except ObjectDoesNotExist:
        data_dict['status'] = 'Invalid Session Key'
        return render_dict_to_response(data_dict)

    # Render it to a the required dict
    data_dict["attributes"] = dict()
    for key, value in service_attributes.items():
        object = user
        attribute = value.split("__")

        # Get the model that the field is a direct member to
        for s in attribute[:-1]:
            object = getattr(object, s)

            # Check if the attribute was a foreignkey
            if hasattr(object, 'count') and object.count() is 1:
                object = object.get()

        # Add the actual attribute to the dict
        data_dict['attributes'][key] = getattr(object, attribute[-1])

    data_dict["status"] = 'Successful'

    return render_dict_to_response(data_dict)


