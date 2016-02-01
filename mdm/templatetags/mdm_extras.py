from django import template


register = template.Library()


@register.filter
def format_number(value, arg):
    if value == None:
        return ""

    return arg % value


@register.filter
def format_date(value):
    if value == None:
        return ""

    return value.strftime("%m/%02d/%Y %l:%02M%p")


@register.filter
def format_percent(value):
    if value == None:
        return "0%"

    return "%d%%" % (value * 100)


@register.filter
def format_model(value, arg):
    models = [
	{ 'name': 'iPad', 'ident': ['iPad1,1'] },
	{ 'name': 'iPad 2', 'ident': ['iPad2,1', 'iPad2,2', 'iPad2,3', 'iPad2,4'] },
	{ 'name': 'iPad Retina', 'ident': ['iPad3,1', 'iPad3,2', 'iPad3,3', 'iPad3,4', 'iPad3,5', 'iPad3,6'] },
	{ 'name': 'iPad Mini', 'ident': ['iPad2,5', 'iPad2,6', 'iPad2,7'] },
	{ 'name': 'iPad Air', 'ident': ['iPad4,1', 'iPad4,2'] },
	{ 'name': 'iPad Mini Retina', 'ident': ['iPad4,4', 'iPad4,5'] },
    ]

    for model in models:
        if value in model['ident']:
            return model['name']

    return arg
