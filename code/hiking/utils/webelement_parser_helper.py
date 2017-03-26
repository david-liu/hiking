import datetime

def get_element_text(web_element):
    value = web_element.text.strip()
    
    if value == u'':
        value = web_element.get_attribute("innerHTML")

    return value

def get_element_attribute(web_element, attribute):
    value = web_element.get_attribute(attribute)

    return value

def format_to_date(date_text, src_format):
    date = datetime.datetime.strptime(date_text, src_format)

    if src_format.find('%Y') == -1:
        date = datetime.date(datetime.datetime.now().year, month=date.month, day=date.day)

    return date
  

def format_to_date_string(date_text, src_format, dest_format='%Y-%m-%d'):
    data_time = format_to_date(date_text, src_format)

    return data_time.strftime(dest_format)

