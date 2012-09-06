import settings

# Name of the centralauth cookie
CENTRALAUTH_COOKIE_NAME_DEFAULT = 'centralauth_session_key_new'
CENTRALAUTH_COOKIE_NAME = getattr(settings, 'CENTRALAUTH_COOKIE_NAME', CENTRALAUTH_COOKIE_NAME_DEFAULT)

# Number of days the cookie can be alive
CENTRALAUTH_COOKIE_DAYS_ALIVE_DEFAULT = 14
CENTRALAUTH_COOKIE_DAYS_ALIVE = getattr(settings, 'CENTRALAUTH_COOKIE_DAYS_ALIVE', CENTRALAUTH_COOKIE_DAYS_ALIVE_DEFAULT)

# The fields that should be sent when a request is made
CENTRALAUTH_USER_ATTRIBUTES_DEFAULT = {
    'username':'username',
    'first_name':'first_name',
    'last_name':'last_name',
    'email':'email',
}
CENTRALAUTH_USER_ATTRIBUTES_DEFAULT = getattr(settings, 'CENTRALAUTH_USER_ATTRIBUTES', CENTRALAUTH_USER_ATTRIBUTES_DEFAULT)

# Sites that have access to this central authentication system
CENTRALAUTH_SERVICES_DEFAULT = (
    #[url, secret_key, user attributes]
)
CENTRALAUTH_SERVICES_DEFAULT = getattr(settings, 'CENTRALAUTH_SERVICES', CENTRALAUTH_SERVICES_DEFAULT)
