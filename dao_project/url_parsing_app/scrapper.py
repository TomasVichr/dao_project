import requests
from bs4 import BeautifulSoup

def requests_url(url):
    error_message_dict = {
            "verbose_label" : "Ok",
            "requests_error" : "none"
            }

    try:
        r = None
        r = requests.get(url,timeout=3)
        r.raise_for_status()

    except requests.exceptions.HTTPError as errh:
        error_message_dict = {
            "verbose_label" : "Requests Http Error",
            "requests_error" : errh
            }
    except requests.exceptions.ConnectionError as errc:
        error_message_dict = {
            "verbose_label" : "Requests Connecting Error",
            "requests_error" : errc
            }
    except requests.exceptions.Timeout as errt:
        error_message_dict = {
            "verbose_label" : "Requests Timeout Error",
            "requests_error" : errt
            }
    except requests.exceptions.RequestException as err:
        error_message_dict = {
            "verbose_label" : "Requests Other Error",
            "requests_error" : err
            }

    return(r, error_message_dict)

def clean_string(my_tag, attribute_css):

    if attribute_css == None:
        return(my_tag.text) #for simple selectors like title, h1, etc.
    else:
        return(my_tag[attribute_css])  #compound css selector: meta, og property


def extract_dict_from_using(my_r, targets_dict):
    output_dict = {}
    soup = BeautifulSoup(my_r.content, 'html.parser')

    for k, v in targets_dict.items():
        is_compound_selector = False

        if isinstance(v, list):
            is_compound_selector = True

        if is_compound_selector == True:
            css_selector, target_attribute = v
        else:
            css_selector = v
            target_attribute = None

        #print(css_selector, target_attribute)
        result_list = soup.select(css_selector)
        number_of_returned_tags = len(result_list)
        output_str = ""

        if number_of_returned_tags > 1:
            output_str = "Not Standard ({} tag results): ".format(number_of_returned_tags)
            output_str = output_str + str(result_list)
        elif number_of_returned_tags == 1:
            output_str = clean_string(result_list[0], target_attribute)
        elif number_of_returned_tags == 0:
            output_str = "Element Not Found"
        else:
            output_str = "Number_of_found_tags: unexpected error"

        output_dict[k] = output_str

    return(output_dict)



