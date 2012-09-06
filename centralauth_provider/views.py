
from models import Session

def validate_service(request):
    #TODO    
    pass

def authenticate(request):
    #TODO: Add check to see if request from internal IP

    # Gather the GET data from request
    session_key = request.GET.get('session_key', None)
    service = request.GET.get('service', None)
    service_key = request.GET.get('service_key', None)

    # Check if all required GET data is available
    if (all((service, service_key, session_key)) is False):
        # TODO: Empty response    
        pass

    # Check if the service is allowed to request an authentication
    if validate_service(service, service_key) is False:
        # TODO: Empty response    
        pass

    # Get session key user
    username = Session.object.get(key=session_key).user.username

    # Return response


def get_service_attributes(service, service_key):
    #TODO    
    pass 

def get_attributes(request):
    #TODO
    # Gather the GET data from request
    session_key = request.GET.get('session_key', None)
    service = request.GET.get('service', None)
    service_key = request.GET.get('service_key', None)

    # Get list of attributes that should be provided
    service_attributes = get_service_attributes(service, service_key)




