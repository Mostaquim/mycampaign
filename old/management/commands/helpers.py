import base64
from quotation.choices import (
    SERVICE_CHOICES,
    PAGE_ORIENTATION,
    PAGES, COLORS,
    TYPE_OF_MEDIA
)
from quotation.models import Format, GSM
import datetime

import pytz


def new_password(encoded):
    salt = encoded[:64]
    hashed_password = encoded[64:]
    try:
        base64_salt = base64.b64encode(bytes.fromhex(salt)).decode('ascii')
        return "%s$%s$%s" % ('old_hash', base64_salt, hashed_password)
    except:
        return "zxlckposefgm234dfgxcvlxcnvio"
        print("password conv error: %s" % encoded)


def old_new_type_service(old_val):
    rel = {
        '1': 1,
        '2': 2,
        '3': 4,
        '4': 3,
        '5': 4,
        '6': 5,
        '7': 6
    }

    return rel[old_val]


def get_page_orientation(old_val):
    if old_val == 'Portrait':
        return 1
    else:
        return 2


def get_page_format(old_val):
    try:
        return Format.objects.get(name=old_val)
    except:
        format_ = Format(name=old_val).save()
        return format_


def get_gsm(old_val):
    try:
        return GSM.objects.get(name=old_val)
    except:
        gsm = GSM(name=old_val).save()
        return gsm


def get_pages(old_val):
    for (val, name) in PAGES:
        if name == old_val:
            return val


def get_color(old_val):
    for (val, name) in COLORS:
        if name == old_val:
            return val


def get_processing(old_val):
    if 'oun' in old_val:
        return 2
    return 1


def validate_date(date_text):
    try:
        return datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except:
        return None


def validate_number(number):
    try:
        return float(number)
    except:
        return 0


def project_name_to_data(text):
    service_type = None
    for(val, name) in SERVICE_CHOICES:
        if name.split()[0] in text:
            service_type = val

    arr = text.split()

    number = int(validate_number(arr[0].replace(',', '')))

    media_type = 4
    for (val, name) in TYPE_OF_MEDIA:
        if name.split()[0] in text:
            media_type = val

    data = {
        'number': number,
        'service': service_type,
        'media': media_type
    }

    return data


def get_time(time):
    time = validate_number(time)
    return datetime.timedelta(seconds=time)


def get_status(text):
    if text == 'can':
        return 6
    elif text == 'cp':
        return 3
    elif text == 'inp':
        return 2
    elif text == 'sus':
        return 4
    else:
        return 1


def get_priority(text):
    if 'High':
        return 3
    elif 'Low':
        return 1
    elif 'Urgent':
        return 4
    else:
        return 1


def unix_to_django_time(timestamp):
    timestamp = validate_number(timestamp)
    time = datetime.datetime.fromtimestamp(timestamp)
    return time


def user_has_no_client(user):
    try:
        client = user.clients
        return False
    except:
        return True


def get_invoice_status(text):
    if text == 'Canceled':
        return 5
    elif text == 'Open':
        return 2
    elif text == 'Paid':
        return 3
    elif text == 'PartiallyPaid':
        return 4
    else:
        return 1


def get_quote_status(text):
    if text == 'Accepted':
        return 3
    elif text == 'Reviewed':
        return 2
    else:
        return 1
