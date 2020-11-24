from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.http import JsonResponse

from datetime import datetime

from .forms import MyForm
from .models import PageInfoModel
from .scrapper import requests_url, extract_dict_from_using


class ParseURLAjax(View):

    def get(self, request):
        form = MyForm()
        context = {"form": form}
        return render(request, "url_parsing_app/index.html", context)

    def post(self, request):
        form = MyForm(request.POST)

        if request.is_ajax():
            if form.is_valid():

                url = request.POST.get('parsed_url')
                my_r, requests_answers = requests_url(url)

                requests_response = requests_answers["verbose_label"]

                feedback_to_user = {
                        "parsed_url": url,
                        }

                if requests_response == "Ok": #if no requests.exceptions.** raised

                    #css selectors for python requests to find
                    searched_selectors_dict = {
                        "title": "title",
                        "h1": "h1", #test
                        "description": ["meta[name=description]", "content"],
                        "site_name": ['meta[property=og\:site_name]', "content"]
                        }
                        #LEGEND; key: CSS selector OR [CSS selector, attribute_to_find]
                        #":" in ['meta[property=og\:site_name]' must be escaped (\)

                    date = datetime.today().strftime('%Y-%m-%d')
                    my_values_dict = extract_dict_from_using(my_r, searched_selectors_dict)


                    page_values_to_save = PageInfoModel(
                        parsed_url = url,
                        title = my_values_dict["title"],
                        description = my_values_dict["description"],
                        site_name = my_values_dict["site_name"],
                        image_url = "placeholder",
                        date = date
                        )
                    page_values_to_save.save()

                    #feedback alert after submitting url
                    feedback_to_user.update({
                        'message_to_user': "URL found and values saved",
                        'title': my_values_dict["title"],
                        'description': my_values_dict["description"],
                        'site_name': my_values_dict["site_name"],
                        'image_url': "placeholder",
                        'date': date,
                        })
                    return JsonResponse(feedback_to_user, status = 200)


                elif requests_response == "Requests Connecting Error": #if requests.exceptions.ConnectionError raised

                    feedback_to_user.update({
                        'message_to_user': "Page does not exist or its server is down. Please check inserted URL",
                        'requests_error_verbose_name': requests_response,
                        'requests_error': str(requests_answers["requests_error"]),
                        })
                    return JsonResponse(feedback_to_user, status = 422) #422 Unprocessable Entity


                elif requests_response == "Requests Http Error": #if requests.exceptions.HTTPError raised

                    feedback_to_user.update({
                        'message_to_user': "Page may exist, but your document was not found. Please check inserted URL",
                        'requests_error_verbose_name': requests_response,
                        'requests_error': str(requests_answers["requests_error"]),
                        })
                    return JsonResponse(feedback_to_user, status = 422) #422 Unprocessable Entity


                else:
                    feedback_to_user.update({
                        'message_to_user': "Unexpected error",
                        'requests_error_verbose_name': requests_response,
                        'requests_error': str(requests_answers["requests_error"]),
                        })
                    return JsonResponse(feedback_to_user, status = 404) #404 Page not found


class GetData(ListView):  #TaskList, is using template/url_parsing_app/task_list.html
    model = PageInfoModel
    queryset = PageInfoModel.objects.order_by('-date') #recent to old

