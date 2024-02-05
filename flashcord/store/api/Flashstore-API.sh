clear
echo [SNWE // Flashstore API] Script Started
cd /System/Websirius/flashcord/store/api
while :
do
	echo [SNWE // Flashstore API] Info: Launching the Flashstore API...
	python3 Flashstore_API-Server-RW.py
	echo [SNWE // Flashstore API] WARNING: Server has crashed or shutted down ! Restarting server automatically in 1 seconds.
	sleep 10
done
echo [SGN-MC] Goodbye.
