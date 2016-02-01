from models import DeviceCommand
from datetime import datetime


command_list = { }
command_snoops = { }


def registerCommandHandler(code, data_handler, result_handler):
    command_list[code] = { 'data': data_handler, 'result': result_handler }


def registerCommandSnooper(code, result_handler):
    list = command_snoops[code]
    if list == None:
        list = [ ]

    list += result_handler
    command_snoops[code] = list


def dataForCommand(command):
    handler = command_list[command.type]
    if handler == None:
        return None

    data = { }
    data['CommandUUID'] = command.uuid
    data['Command'] = handler['data'](command)

    return data


def handleCommandResponse(command, response):
    if command.type not in command_list:
        return False
    handler = command_list[command.type]
    if handler == None or 'result' not in handler or handler['result'] == None:
        return False

    if handler['result'](command, response) != True:
        return False

    # Let any snoopers run
    if command.type not in command_snoops:
        return True
    list = command_snoops[command.type]
    with snoop in list:
        snoop(command, response)

    return True
