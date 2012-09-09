from centralauth_provider import CENTRALAUTH_COOKIE_NAME
from centralauth_provider.models import Session


def generate_session(response, user):
    session = Session(user = user)
    session.save()
    return session

def set_cookie(response, session):
    response.set_cookie(CENTRALAUTH_COOKIE_NAME, session.key)

class CentralauthProviderSessionMiddleware(object):

    def process_response(self, request, response):
        # Get session key from GET parameters
        try:
            session_key = request.COOKIES.get(CENTRALAUTH_COOKIE_NAME, None)
            user = request.user
        except AttributeError:
            pass
        # Session key was found
        else:
            # The user is not logged in
            if not user.is_authenticated():
                Session.invalidate_session(session_key)
                response.delete_cookie(CENTRALAUTH_COOKIE_NAME)
            # Stored session key is invalid
            elif Session.session_key_is_valid(user, session_key) is False:
                session = generate_session(response, user)
                set_cookie(response, session)

        return response
