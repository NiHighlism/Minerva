[0;1;32m●[0m minerva.service - uWSGI instance to serve minerva
   Loaded: loaded (/etc/systemd/system/minerva.service; enabled; vendor preset: enabled)
   Active: [0;1;32mactive (running)[0m since Fri 2020-05-01 20:10:16 UTC; 16min ago
 Main PID: 2178 (uwsgi)
    Tasks: 17 (limit: 4915)
   CGroup: /system.slice/minerva.service
           ├─2178 /home/metamehta/minerva/env/bin/uwsgi --ini minerva_wsgi.ini
           ├─2208 /home/metamehta/minerva/env/bin/uwsgi --ini minerva_wsgi.ini
           ├─2209 /home/metamehta/minerva/env/bin/uwsgi --ini minerva_wsgi.ini
           ├─2213 /home/metamehta/minerva/env/bin/uwsgi --ini minerva_wsgi.ini
           └─2218 /home/metamehta/minerva/env/bin/uwsgi --ini minerva_wsgi.ini

May 01 20:10:16 minerva systemd[1]: Started uWSGI instance to serve minerva.
May 01 20:10:16 minerva uwsgi[2178]: [uWSGI] getting INI configuration from minerva_wsgi.ini
