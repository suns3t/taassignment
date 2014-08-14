import ldap
from django.conf import settings

def get_ldap_user_data(username):
    try:
        # Check if this username is an valid Odin username
        ld = ldap.initialize(settings.LDAP_URL)
        ld.simple_bind_s()
        results = ld.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "uid=" + username)
        record = results[0][1]
    except IndexError:
        return None, None

    cn = record['cn']
    parts = cn[0].split(" ")
    first_name = parts[0]
    last_name = " ".join(parts[1:])
    return first_name, last_name
