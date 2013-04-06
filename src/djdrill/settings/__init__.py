import socket
from django.core.exceptions import ImproperlyConfigured

hostname = socket.gethostname()

if hostname == "arun-desktop":
    from settings_arun import *
elif hostname == "Leoankit":
    from settings_ankit import *
#elif hostname == "leo-desktop": 
#    from  import *
elif hostname == "Leonilesh":
    from settings_nilesh import *
else:
    raise ImproperlyConfigured("No settings module found for host: %s" % hostname)

del(hostname)
