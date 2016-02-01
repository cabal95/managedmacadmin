from APNSWrapper import *
import base64

token = base64.b64decode('tuAjccOSU0aMqd+0TITgzVbUk3m2UjsrcJa3PQCYvOU=')
magic = '58489227-0A45-4F8B-8838-1EE94C848135'
topic = 'com.apple.mgmt.External.89ac8a6a-4780-4825-8b8d-0a148f40c795'

wrapper = APNSNotificationWrapper('pushcert.pem', False)

message = APNSNotification()
message.token(token)
message.appendProperty(APNSProperty('mdm', magic))
wrapper.append(message)
if (wrapper.notify()):
  print 'Message sent successfully'
else:
  print 'Failed to send push notification'

