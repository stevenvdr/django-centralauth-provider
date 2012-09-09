import json

#from django.db.models.fields.related import RelatedManager
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from centralauth_provider import *
from centralauth_provider.models import Session

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
    return HttpResponse(content="<body>"+json.dumps(data_dict)+"</body>")
    

def authenticate(request):
    #TODO: Add check to see if request from internal IP

    # Gather the GET data from request
    session_key = request.GET.get('session_key', None)
    service = request.GET.get('service', None)

    data_dict = dict()

    # Check if all required GET data is available
    if (all((service, session_key)) is False):
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
    if (all((service, session_key)) is False):
        data_dict['status'] = 'Incorrect request'
        return render_dict_to_response(data_dict)

    # Check if the service is allowed to request an authentication
    elif validate_service(service) is False:
        data_dict['status'] = 'Invalid service'
        return render_dict_to_response(data_dict)


    # Get list of attributes that should be provided
    service_attributes = get_service_attributes(service)
    attributes = service_attributes.values()

    # Get user data from database
    #user_data = User.objects.filter(sessions__key=session_key).values() #*attributes)
    user = User.objects.get(sessions__key=session_key)

    # Check if a user was found
    #if len(user_data) == 1:
    #    user_data = user_data[0]
    #else:
    #    data_dict['status'] = 'Invalid Session Key'
    #    return render_dict_to_response(data_dict)

    # Render it to a the required dict
    data_dict["attributes"] = dict()
    for key, value in service_attributes.items():
        object = user
        attribute = value.split("__")
        try:
            for s in attribute[:-1]:
                object = object.__getattribute__(s)

                # If the object is a related manager, fetch the real object
                if hasattr(object, 'get'):
                    object = object.get()

            data_dict["attributes"][key] = object.__getattribute__(attribute[-1])

        except ObjectDoesNotExist:
            data_dict["attributes"][key] = None

    data_dict["status"] = 'Successful'

    return render_dict_to_response(data_dict)


