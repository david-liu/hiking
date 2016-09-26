import datetime

def get_element_text(web_element):
    value = web_element.text.strip()
    
    if value == u'':
        value = web_element.get_attribute("innerHTML")

    return value

def format_to_date(date_text, src_format):
    return datetime.datetime.strptime(date_text, src_format)

def format_to_date_string(date_text, src_format, dest_format='%Y-%m-%d'):
    data_time = format_to_date(date_text, src_format)

    return data_time.strftime(dest_format)

