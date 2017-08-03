Running server when connected to NU-Wave via ethernet:
	$ hostname -I   #to optain ip
	$ python manage.py runserver {{ ip address }}:80

Access site while on nu wave at ip address


Versions:
Python - 3.4.2
Django - 1.9.8 (pip install django==1.9.8)

Create Professor user:
python manage.py createsuperuser

Requirements for chat:
Channels (pip install channels)
Asgi_redis (pip install asgi_redis)
Redis server (http://redis.io/download)
Haikunator(for random url generation ) pip install haikunator

Running server with chat app:
Run redis first ($redis-server)
start the channels layer ($daphne config_classio.asgi:channel_layer --port 8888)
Run django ($python manage.py runworker)
go to localhost:8888/new and a new chat room will be created

sudo apt install screen

Run server using new script: bash START.sh
