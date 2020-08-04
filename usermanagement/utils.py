

def convert_to_slots(data):
    return_list = []
    for _ in data:
        if not any( date['date'] == _['slot'].date() for date in return_list):
            return_list.append({'date':_['slot'].date(), 'slot':[_['slot'].strftime('%H:%M:%S')]})
        else:
            dict_to_append = next((item for item in return_list if item['date'] == _['slot'].date()), None)
            dict_to_append['slot'].append(_['slot'].strftime('%H:%M:%S'))
    return return_list

