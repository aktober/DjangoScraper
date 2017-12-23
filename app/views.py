import datetime
import json

import re

import requests
from django.http import JsonResponse
from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.views import APIView

from DjangoScraper._celery import run_task, task_with_param
from app import models
from app import utils

from DjangoScraper import settings
from app.serializers import NewsSerializer

APIKEY = 'apikey ' + settings.MAILCHIMP_API_KEY
BASE_URL = 'https://' + settings.MAILCHIMP_DC + '.api.mailchimp.com/3.0/lists/'
TEMPLATE_URL = 'https://' + settings.MAILCHIMP_DC + '.api.mailchimp.com/3.0/templates'
TEMPLATE_ID = settings.MAILCHIMP_TEMPLATE_ID

summary = dict()


class HomePage(generic.View):

    def get(self, request):
        # task_with_param.s('test').delay()
        # task_with_param.delay(param='x', countdown=20)
        task_with_param.apply_async(args=['hello'], countdown=10)
        return render(request, 'app/home.html')


class DashboardPage(generic.View):

    def get(self, request):
        # market recap
        market_cap, btc_dominance = utils.get_current_market_and_dominance()
        market_week_ago = utils.get_market_week_ago()
        dominance_week_ago = utils.get_dominance_week_ago()
        market_cap_diff = utils.get_value_diff(market_cap, market_week_ago)
        btc_dominance_diff = utils.get_value_diff(btc_dominance, dominance_week_ago)

        best, worse = utils.get_best_worse_currencies()
        btc_low, btc_high = utils.get_low_high_btc_week_price()

        today = datetime.datetime.now()
        today_str = today.strftime("%m/%d/%Y")

        summary['report_date'] = today_str
        summary['market_cap'] = "{:,}".format(market_cap)
        summary['market_cap_diff'] = "{0:.2f}".format(market_cap_diff)
        summary['market_cap_is_up'] = True if market_cap_diff > 0 else False
        summary['btc_low'] = btc_low
        summary['btc_high'] = btc_high
        summary['btc_dominance'] = btc_dominance
        summary['btc_dominance_diff'] = "{0:.2f}".format(btc_dominance_diff)
        summary['best'] = best
        summary['worse'] = worse

        qs = models.NewsModel.objects.all()
        selected_news = models.NewsModel.objects.filter(use_in_report=True)

        context = {
            # for report
            'report_date': today_str,
            'market_cap': "{:,}".format(market_cap),
            'market_cap_diff': "{0:.2f}".format(market_cap_diff),
            'market_cap_is_up': True if market_cap_diff > 0 else False,

            'btc_low': btc_low,
            'btc_high': btc_high,

            'btc_dominance': btc_dominance,
            'btc_dominance_diff': "{0:.2f}".format(btc_dominance_diff),
            'btc_dominance_is_up': True if btc_dominance_diff > 0 else False,

            'best': best,
            'worse': worse,

            'weekly_news': selected_news,

            # for weekly news
            'data': qs,
        }
        return render(request, 'app/dashboard.html', context)


def get_subscribers_list():
    headers = {
        'Authorization': APIKEY
    }
    url = BASE_URL + settings.MAILCHIMP_LIST_ID + '/members'
    r = requests.get(url, headers=headers)
    parsed = r.json()
    members = _get_member_list(parsed)
    return members


def _get_member_list(parsed):
    members = []
    for member in parsed['members']:
        d = {
            'email': member['email_address'],
            'status': member['status'],
            'id': member['id'],
        }
        members.append(d)
    return members


@csrf_exempt
def ajax_unsubscribe(request):
    if request.POST:
        id = request.POST.get('id')
        headers = {
            'Authorization': APIKEY
        }
        delete_url = BASE_URL + settings.MAILCHIMP_LIST_ID + '/members/' + id
        requests.delete(delete_url, headers=headers)

        url = BASE_URL + settings.MAILCHIMP_LIST_ID + '/members'
        data = requests.get(url, headers=headers)
        parsed = data.json()
        members = _get_member_list(parsed)

    return JsonResponse(members, safe=False)


@csrf_exempt
def ajax_subscribe(request):
    if request.POST:
        email = request.POST.get('email')
        headers = {
            'Authorization': APIKEY
        }
        url = BASE_URL + settings.MAILCHIMP_LIST_ID + '/members'
        subscribe_data = {
            "email_address": email,
            "status": "subscribed",
        }
        requests.post(url, headers=headers, data=json.dumps(subscribe_data))

        get_data = requests.get(url, headers=headers)
        parsed = get_data.json()
        members = _get_member_list(parsed)

    return JsonResponse(members, safe=False)


class NewsList(generics.ListAPIView):
    queryset = models.NewsModel.objects.all()
    serializer_class = NewsSerializer


class NewsUpdate(APIView):
    queryset = models.NewsModel.objects.all()
    serializer_class = NewsSerializer
    permission_classes = []
    authentication_classes = []

    def get_object(self, pk):
        return models.NewsModel.objects.get(pk=pk)

    def patch(self, request, *args, **kwargs):
        pk = request.data['id']
        obj = self.get_object(pk)
        serializer = NewsSerializer(obj, data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data='ok', safe=False)
        return JsonResponse(code=400, data="wrong parameters", safe=False)


@csrf_exempt
def ajax_filter(request):
    if request.POST:
        r = request.POST
        qs = models.NewsModel.objects.all()

        if 'text' in r and r.get('text'):
            text = r.get('text')
            qs = qs.filter(title__icontains=text)

        if 'category' in r and r.get('category'):
            category = r.get('category')
            qs = qs.filter(category__icontains=category)

        if 'comments' in r and r.get('comments'):
            comments_filter = r.get('comments')
            if '<' in comments_filter:
                number = re.sub('[<>=]', '', comments_filter)
                qs = qs.filter(comments__lte=number)

            if '>' in comments_filter:
                number = re.sub('[<>=]', '', comments_filter)
                qs = qs.filter(comments__gte=number)

        if 'votes' in r and r.get('votes'):
            votes_filter = r.get('votes')
            if '<' in votes_filter:
                number = re.sub('[<>=]', '', votes_filter)
                qs = qs.filter(votes__lte=number)

            if '>' in votes_filter:
                number = re.sub('[<>=]', '', votes_filter)
                qs = qs.filter(votes__gte=number)

        if 'sort' in r and r.get('sort'):
            sort_by = r.get('sort')
            qs = qs.order_by(sort_by)

        result = render_to_string('app/ajax_filter.html', context={'data': qs})
        return JsonResponse({'html': result})


def ajax_get_news(request):
    if request.GET:
        pk = request.GET.get('pk')
        obj = models.NewsModel.objects.get(pk=pk)
        serializer = NewsSerializer(obj)
        return JsonResponse(data=serializer.data, safe=False)


@csrf_exempt
def submit_report(request):
    if request.is_ajax():
        selected_news = models.NewsModel.objects.filter(use_in_report=True)
        context = {
            'weekly_news': selected_news,
            'summary': summary,
        }
        html = render_to_string('app/email_template.html', context)

        headers = {
            'Authorization': APIKEY
        }
        template_data = {
            "name": 'new template',
            "html": html,
        }

        requests.patch(TEMPLATE_URL + '/' + TEMPLATE_ID, headers=headers,
                       data=json.dumps(template_data))

        return JsonResponse(data='ok', safe=False)


def report_weekly_news(request):
    if request.is_ajax():
        qs = models.NewsModel.objects.filter(use_in_report=True)
        result = render_to_response('app/ajax_weekly_news.html', context={'weekly_news': qs})
        return result


def ajax_get_subscribers(request):
    if request.is_ajax():
        members = get_subscribers_list()
        return JsonResponse(data=members, safe=False)


def ajax_run_crawl(request):
    if request.is_ajax():
        run_task.delay()
        return JsonResponse(data='Ok', safe=False)