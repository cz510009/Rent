from os import name
from django.http.response import HttpResponse
from numpy import add
import requests
from bs4 import BeautifulSoup
import pandas as pd
from django.template import loader
import re
from django.shortcuts import render
from django.views import View
from django import forms
from requests.api import get
from . import forms
from .models import Rent
from django.http import QueryDict
from .models import Rent

sfitUrl = "http://sfit-search.jp/rent/search/?cn=20&co_knh=1&ct=15.0&et=15&kz=1&md=01&md=02&md=03&md=04&md=05&md=06&order=6&page={}&rows=50&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13106&sc=13107&sc=13108&sc=13109&sc=13110&sc=13111&sc=13112&sc=13113&sc=13114&sc=13115&sc=13116&sc=13117&sc=13118&sc=13119&sc=13120&sc=13121&sc=13122&sc=13123&tc=0400301&tc=0400101&tc=0401303"
suumoUrl = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&fw2=&pc=30&po1=25&po2=99&ta=13&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&sc=13106&sc=13107&sc=13108&sc=13118&sc=13121&sc=13122&sc=13123&sc=13109&sc=13110&sc=13111&sc=13112&sc=13114&sc=13115&sc=13120&sc=13116&sc=13117&sc=13119&md=02&md=03&md=04&md=05&cb=0.0&ct=15.0&et=20&mb=0&mt=65&cn=25&co=1&co=3&co=4&kz=1&tc=0401303&tc=0400101&tc=0400103&tc=0400502&tc=0400601&tc=0400301&tc=0400302&tc=0400303&tc=0401101&tc=0401106&shkr1=03&shkr2=03&shkr3=03&shkr4=03&page={}"


def getHtml(url):
    response = requests.get(url)
    bs = BeautifulSoup(response.content, "html.parser")
    return bs


rentInfo = {'category': [], 'name': [], 'address': [], 'layout': [], 'rent': [], 'area': [],
            'station': [], 'timeOnFoot': [], 'age': [], 'url': [], 'difference': [], 'bargain': []}

average = {'千代田区': {'1R': 6.6, '1K, 1DK': 8.7, '1LDK, 2K, 2DK': 16.7}, '中央区': {'1R': 8.2, '1K, 1DK': 9.5, '1LDK, 2K, 2DK': 14.3}, '港区': {'1R': 7.5, '1K, 1DK': 9.7, '1LDK, 2K, 2DK': 17.5}, '新宿区': {'1R': 7.5, '1K, 1DK': 8.9, '1LDK, 2K, 2DK': 14.3}, '文京区': {'1R': 7.7, '1K, 1DK': 8.8, '1LDK, 2K, 2DK': 13.2}, '台東区': {'1R': 7.8, '1K, 1DK': 8.7, '1LDK, 2K, 2DK': 12.4}, '墨田区': {'1R': 7.2, '1K, 1DK': 8.1, '1LDK, 2K, 2DK': 11.5}, '江東区': {'1R': 7.3, '1K, 1DK': 8.2, '1LDK, 2K, 2DK': 11.5}, '品川区': {'1R': 7.8, '1K, 1DK': 8.9, '1LDK, 2K, 2DK': 13.1}, '目黒区': {'1R': 7.7, '1K, 1DK': 8.9, '1LDK, 2K, 2DK': 13.5}, '大田区': {'1R': 6.7, '1K, 1DK': 7.6, '1LDK, 2K, 2DK': 10.8}, '世田谷区': {'1R': 7.0, '1K, 1DK': 8.0, '1LDK, 2K, 2DK': 11.6},
           '渋谷区': {'1R': 7.8, '1K, 1DK': 9.5, '1LDK, 2K, 2DK': 16.2}, '中野区': {'1R': 7.5, '1K, 1DK': 8.2, '1LDK, 2K, 2DK': 11.2}, '杉並区': {'1R': 6.8, '1K, 1DK': 7.6, '1LDK, 2K, 2DK': 12.1}, '豊島区': {'1R': 6.9, '1K, 1DK': 8.0, '1LDK, 2K, 2DK': 12.1}, '北区': {'1R': 6.4, '1K, 1DK': 7.2, '1LDK, 2K, 2DK': 10.4}, '荒川区': {'1R': 6.8, '1K, 1DK': 7.5, '1LDK, 2K, 2DK': 10.4}, '板橋区': {'1R': 6.2, '1K, 1DK': 6.8, '1LDK, 2K, 2DK': 9.3}, '練馬区': {'1R': 6.1, '1K, 1DK': 6.7, '1LDK, 2K, 2DK': 9.2}, '足立区': {'1R': 5.8, '1K, 1DK': 6.3, '1LDK, 2K, 2DK': 8.3}, '葛飾区': {'1R': 5.7, '1K, 1DK': 6.2, '1LDK, 2K, 2DK': 8.0}, '江戸川区': {'1R': 5.6, '1K, 1DK': 6.2, '1LDK, 2K, 2DK': 8.4}}


def getRentInfoFromSFit():
    nextPageFlag = True
    pageCount = 1
    while nextPageFlag:
        targetUrl = sfitUrl.format(pageCount)
        html = getHtml(targetUrl)
        next = html.select("div.pagination li.next a")
        # 次へのリンクがなければ最終ページ
        if len(next) == 0:
            nextPageFlag = False
        pageCount += 1
        rentList = html.findAll("div", {"class": "frList"})
        for rent in rentList:
            rentInfo["category"].append('S-FIT')
            name = rent.find(
                "a", {"class": "link-to-detail"}).getText().strip()
            rentInfo["name"].append(name)
            address = rent.find("div", {"class": "jusho"}).getText().strip()
            rentInfo["address"].append(address)
            monthlyRent = rent.find(
                "div", {"class": "chinryo"}).getText().strip()
            rentInfo["rent"].append(float(monthlyRent.replace(
                '万円', '')))
            divs = rent.select("td div")
            area = divs[8].getText().strip().replace('m2', '')
            rentInfo["area"].append(float(area))
            layout = divs[7].getText().strip().replace('m2', '')
            if layout == 'ワンルーム':
                layout = "1R"
            if 'S' in layout:
                layout = layout.replace('S', '')
            rentInfo["layout"].append(layout)
            age = divs[11].getText().strip()
            if age == '新築':
                rentInfo["age"].append(0)
            else:
                age = age.replace('築', '')
                age = age.replace('年', '')
                rentInfo["age"].append(int(age))
            rentInfo["station"].append(divs[13].getText().strip())
            timeOnFoot = divs[14].getText().strip().replace('徒歩 ', '')
            rentInfo["timeOnFoot"].append(
                int(timeOnFoot.replace('分', '')))
            url = "http://sfit-search.jp" + \
                rent.find("a", {"class": "link-to-detail"}).get("href")
            rentInfo["url"].append(url)
            for key in average.keys():
                if key in address:
                    for layoutKey in average[key].keys():
                        if layout in layoutKey:
                            stripped = monthlyRent.replace(
                                '万円', '')
                            floatRent = float(stripped)
                            difference = floatRent - \
                                average[key][layoutKey]
                            rentInfo["difference"].append(
                                round(difference, 2))
                            stripped = timeOnFoot.replace('分', '')
                            intTime = int(stripped)
                            if intTime <= 10 and difference < 0:
                                rentInfo["bargain"].append(True)
                            else:
                                rentInfo["bargain"].append(False)


def getRentInfoFromSuumo():
    nextPageFlag = True
    pageCount = 1
    while nextPageFlag:
        targetUrl = suumoUrl.format(pageCount)
        html = getHtml(targetUrl)
        pagination = html.select("p.pagination-parts a")
        if len(pagination) == 1 and pagination[0].getText() == "前へ":
            nextPageFlag = False
        pageCount += 1
        rentList = html.findAll("div", {"class": "cassetteitem"})
        for rent in rentList:
            name = rent.find(
                "div", {"class": "cassetteitem_content-title"}).getText().strip()
            address = rent.find(
                "li", {"class": "cassetteitem_detail-col1"}).getText().strip()
            age = rent.find(
                "li", {"class": "cassetteitem_detail-col3"}).contents[1].getText().strip()
            stationAndTimeOnFoot = rent.find(
                "div", {"class": "cassetteitem_detail-text"}).getText().strip()
            timeOnFoot = re.sub(
                '(.*)(?=歩)', '', stationAndTimeOnFoot).replace('歩', '')
            station = re.sub('(?<=歩)(.*)', '',
                             stationAndTimeOnFoot).replace(' 歩', '')
            rooms = rent.select("tbody tr.js-cassette_link")
            for room in rooms:
                rentInfo["category"].append('SUUMO')
                rentInfo["name"].append(name)
                rentInfo["address"].append(address)
                rentInfo["timeOnFoot"].append(int(timeOnFoot.replace('分', '')))
                rentInfo["station"].append(station)
                if age == '新築':
                    rentInfo["age"].append(0)
                else:
                    age = age.replace('築', '')
                    age = age.replace('年', '')
                    rentInfo["age"].append(int(age))
                monthlyRent = room.contents[7].find(
                    "span", {"class": "cassetteitem_other-emphasis ui-text--bold"}).getText().strip().replace('万円', '')
                rentInfo["rent"].append(float(monthlyRent))
                area = room.contents[11].find(
                    "span", {"class": "cassetteitem_menseki"}).getText().strip().replace('m2', '')
                rentInfo["area"].append(float(area))
                layout = area = room.contents[11].find(
                    "span", {"class": "cassetteitem_madori"}).getText().strip()
                if layout == 'ワンルーム':
                    layout = "1R"
                rentInfo["layout"].append(layout)

                for key in average.keys():
                    if key in address:
                        for layoutKey in average[key].keys():

                            if layout in layoutKey:
                                stripped = monthlyRent.replace(
                                    '万円', '')
                                floatRent = float(stripped)
                                difference = floatRent - \
                                    average[key][layoutKey]
                                rentInfo["difference"].append(
                                    round(difference, 2))
                                stripped = timeOnFoot.replace('分', '')
                                intTime = int(stripped)
                                if intTime <= 10 and difference < 0:
                                    rentInfo["bargain"].append(True)
                                else:
                                    rentInfo["bargain"].append(False)

                url = "https://suumo.jp" + room.find(
                    'a', {"class": "cassetteitem_other-linktext"}).get("href")
                rentInfo["url"].append(url)


df = pd.DataFrame(index=[], columns=[])


def home(request):
    conditions = {
        'text': request.GET.get('text'),
        'bargain': bool(request.GET.get('bargain')),
        'diff': bool(request.GET.get('diff')),
        'lower': request.GET.get('lower'),
        'upper': request.GET.get('upper'),
        'time': request.GET.get('time'),
        'lowerArea': request.GET.get('lowerArea'),
        'upperArea': request.GET.get('upperArea'),
        'age': request.GET.get('age')
    }

    getRentInfoFromSFit()

 #   getRentInfoFromSuumo()
    df = pd.DataFrame(rentInfo)
    if conditions['lower'] != '0':
        l = conditions['lower']
        toFloat = float(l)
        df = df[df['rent'] >= toFloat]

    if conditions['upper'] != '0':
        l = conditions['upper']
        toFloat = float(l)
        df = df[df['rent'] <= toFloat]

    if conditions['time'] != '0':
        l = conditions['time']
        toInt = int(l)
        df = df[df['timeOnFoot'] <= toInt]

    if conditions['bargain'] == True:
        df = df[df['bargain'] == True]

    if conditions['age'] != '0':
        l = conditions['age']
        toInt = int(l)
        df = df[df['age'] <= toInt]

    if conditions['lowerArea'] != '0':
        l = conditions['lowerArea']
        toInt = float(l)
        df = df[df['area'] >= toInt]

    if conditions['upperArea'] != '0':
        l = conditions['upperArea']
        toInt = float(l)
        df = df[df['area'] <= toInt]

    if conditions['text'] != None:
        conditions['text'] = conditions['text'].split()
        if len(conditions['text']) > 0:
            tempDf = pd.DataFrame(index=[], columns=[])
            for t in conditions['text']:
                copy = df
                index = df.index[~df['address'].str.contains(
                    t)]
                if index.size != 0:
                    getDf = df.drop(index)
                    tempDf = pd.concat([tempDf, getDf])
                index = df.index[~df['station'].str.contains(
                    t)]
                if index.size != 0:
                    getDf = df.drop(index)
                    tempDf = pd.concat([tempDf, getDf])
            df = tempDf
    df = df.sort_values(by=['rent'], ascending=True)
    print(df.columns)
    template = loader.get_template('home.html')
    json = df.to_json(force_ascii=False)
    context = {'df': df, 'json': json}
    return HttpResponse(template.render(context, request))


def search(request):
    lower = forms.LowerChoiceForm()
    upper = forms.UpperChoiceForm()
    time = forms.TimeChoiceForm()
    lArea = forms.LowerAreaChoiceForm()
    upperArea = forms.UpperAreaChoiceForm()
    age = forms.AgeChoiceForm()

    context = {
        'lower': lower,
        'upper': upper,
        'time': time,
        'lArea': lArea,
        'upperArea': upperArea,
        'age': age
    }
    return render(request, 'search.html', context)


def for_ajax(request):    # AJAXに答える関数
    import json
    from django.http import HttpResponse, Http404

    if request.method == 'POST':
        from django.http import QueryDict
        from .models import Rent
        dic = QueryDict(request.body, encoding='utf-8')
        category = dic.get('category')
        name = dic.get('name')
        url = dic.get('url')
        address = dic.get('address')
        rent = dic.get('rent')
        layout = dic.get('layout')
        area = dic.get('area')
        station = dic.get('station')
        timeOnFoot = dic.get('timeOnFoot')
        age = dic.get('age')
        difference = dic.get('difference')
        bargain = dic.get('bargain')
        if bargain == 'false':
            bargain = False
        else:
            bargain = True
        user = request.user
        db = Rent(user=user, category=category, name=name, url=url, address=address, rent=rent, layout=layout,
                  area=area, station=station, timeOnFoot=timeOnFoot, age=age, difference=difference, bargain=bargain)
        db.save()
        return HttpResponse("登録しました")


def favorite(request):
    from .models import Rent
    data = Rent.objects.all().filter(user=request.user)
    context = {
        'data': data
    }
    return render(request, 'favorite.html', context)


def delete(request):
    if request.method == 'POST':
        dic = QueryDict(request.body, encoding='utf-8')
        id = dic.get('id')
        Rent.objects.filter(id=id).delete()
        return HttpResponse("削除しました")


# def localStorage(request):    # AJAXに答える関数
#     import json
#     from django.http import HttpResponse,Http404

#     if request.method == 'POST':
#         from django.http import QueryDict
#         from .models import Rent
#         dic = request.GET.get('data'),

#         return dic

# import ast

# from django.http import JsonResponse
# def ajax(request):
#     data = request.GET.get('ls')
#     data = data.replace('[','')
#     data = data.replace(']','')
#     data =re.sub('^"','',data)
#     data =re.sub('"$','',data)
#     data = re.split('(?<=}).*?(?={)', data)
#     rentInfo = {'category': [], 'name': [], 'address': [], 'layout': [], 'rent': [], 'area': [],
#             'station': [], 'timeOnFoot': [], 'age': [], 'url': [], 'difference': [], 'bargain': []}
#     for d in data:
#         d = d.replace('\\','')
#         d = json.loads(d)
#         rentInfo['category'].append(d['category'])
#         rentInfo['name'].append(d['name'])
#         rentInfo['address'].append(d['address'])
#         rentInfo['layout'].append(d['layout'])
#         rentInfo['rent'].append(d['rent'])
#         rentInfo['area'].append(d['area'])
#         rentInfo['station'].append(d['station'])
#         rentInfo['timeOnFoot'].append(d['timeOnFoot'])
#         rentInfo['age'].append(d['age'])
#         rentInfo['url'].append(d['url'])
#         rentInfo['difference'].append(d['difference'])
#         rentInfo['bargain'].append(d['bargain'])
#     for key in rentInfo.keys():
#         print(len(rentInfo[key]))
#     df = pd.DataFrame(rentInfo)
#     context = {
#         'df':df
#     }
#     return context
