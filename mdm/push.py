from APNSWrapper import *
import base64
from models import Device
from datetime import datetime


def push_notification(dev):
    dev.last_notification = datetime.now()
    dev.save()

    token = base64.b64decode(dev.push_token)
    magic = str(dev.push_magic)
    topic = str(dev.push_topic)

    wrapper = APNSNotificationWrapper('/var/mdm/env/managedmacadmin/mdm/pushcert.pem', False)

    message = APNSNotification()
    message.token(token)
    message.appendProperty(APNSProperty('mdm', magic))
    wrapper.append(message)

    return wrapper.notify()

