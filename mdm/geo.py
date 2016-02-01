import urllib2
import json


#
# Geocode the given IP address. Return a dictionary with the following
# keys:
#	latitude	[required]
#	longitude	[required]
#	country_code	[required]
#	region_code	[required]
#	city		[required]
#	country_name	[optional]
#	region_name	[optional]
#
# Any required fields that are unavailable should exist but be blank
# strings.
#	
#{"ip":"24.182.14.97","country_code":"US","country_name":"United States","region_code":"CA","region_name":"California","city":"Hesperia",
#"zipcode":"","latitude":34.4264,"longitude":-117.3009,"metro_code":"803","area_code":"760"}
def geocode(ip):
    socket = None
    data = {
	'latitude': 0,
	'longitude': 0,
	'country_code': '',
	'region_code': '',
	'city': '' };

    try:
        socket = urllib2.urlopen("http://freegeoip.net/json/" + ip, None, 2)
        result = json.loads(socket.read())

        data['latitude'] = result['latitude']
        data['longitude'] = result['longitude']
        data['country_code'] = result['country_code']
        data['region_code'] = result['region_code']
        data['city'] = result['city']
        data['country_name'] = result['country_name']
        data['region_name'] = result['region_name']
    except:
        if socket == None:
            try:
                socket.close()
            except:
                pass
        pass

    return data

