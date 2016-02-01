Managed Mac Admin is a Python/VirtualEnv based MDM server.

This was a project I worked on a few years ago. In the end we decided
to move to a 3rd party commercial MDM solution. Not because this one
did not work well but because my position changed and I was no longer
going to be doing programming and wouldn't be able to keep the system
maintained. We ran this system for about 9 months with no functional
problems, so it does work, though it still needs a lot of TLC if you
plan to use it in a production environment.


To get up and running (no promises, most of this is from memory):

Needed manual update to APNSWrapper to support TLS.
	in connection.py change PROTOCOL_SSLv3 to PROTOCOL_SSLv23

From your virtual environment, run:

python manage.py syncdb
chmod a+w db.sqlite3 (web server needs write access)
python manage.py migrate
python manage.py collectstatic

You should now be able to login to the MDM server.
Go to the Config section and Configure your Certificate Authority.

You should now be able to enroll devices.

To enable Push-Notifications to work, you need to create your push
certificate and call it "pushcert.pem" then place it in the mdm
directory.
