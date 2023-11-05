from django.shortcuts import render
from django.shortcuts import render, redirect
from datetime import datetime
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password, check_password
from user.models import Board, Member, Diary
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from summary import *
import pandas as pd
import numpy as np
import re
import networkx
from konlpy.tag import Komoran
import os
import openai

import translate
from translate.Transformer import *

from translate.Transformer import predict
import argparse
import torch

from translate.Transformer.data import *
from translate.Transformer.model.transformer import Transformer

from base64 import b64decode
from IPython import display
from PIL import Image
from io import BytesIO

from googletrans import Translator
import time

from elasticsearch import Elasticsearch
import json
from django.core import serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from elasticsearch import Elasticsearch


diary_check_openai_api_key = # Place your API keys here
tts_diary_client_id = # Place your client id here
tts_diary_secret_key = # Place your API keys here


def home_view(request):
    return render(request, "MalLang/home.html")

def main_view(request):
    nickname = request.session.get("nickname")
    user_id = request.session.get("user_id")

    context = {
        'nickname': nickname,
        'user_id': user_id
    }
    return render(request, "MalLang/main.html", context)


def diary_view(request):
    today = datetime.today().date()
    nickname = request.session.get("nickname")
    user_id = request.session.get("user_id")

    context = {
        'today': today,
        'nickname': nickname,
        'user_id': user_id
    }
    return render(request, "MalLang/diary.html", context)



def diary_check(request):
    nickname = request.session.get("nickname")
    user_id = request.session.get("user_id")

    if request.method == 'POST':
        date = request.POST.get('date')
        weather = request.POST.get('weather')
        emoji = request.POST.get('emoji')
        diary = request.POST.get('diary')

        # 요약
        summary = get_summary_from_text(diary)
        print('요약:' + summary)
        # 번역
        n_input_vocab = len(vocab_ko)
        n_output_vocab = len(vocab_en)
        
        model = Transformer(n_input_vocab=n_input_vocab,
                            n_output_vocab=n_output_vocab,
                            n_layers=n_layers,
                            d_model=d_model,
                            d_ff=d_ff,
                            head=head,
                            dropout=dropout,
                            max_len=max_len,
                            padding_idx=padding_idx,
                            device=device).to(device)
        
        
        text = summary
        
        # model load
        try:
            latest_version = sorted(os.listdir(f'{save_path}saved'))
            for version in latest_version:
                if version[-3:] == ".pt":
                    latest_version = version
                    break
            model.load_state_dict(torch.load(f'{save_path}saved/{latest_version}', map_location=torch.device('cpu')))
        except Exception as e:
            raise SystemExit(e)
        
        text = predict.predict(model, text)

        text2 = Translator()
        res = text2.translate(summary, src='ko', dest='en')
        res = res.text
        print("번역:"+text)
        print("번역2:"+res)
        
        # 그림
        openai.api_key = diary_check_openai_api_key

        # 번역 모델에 대한 이미지
        PROMPT_text = text + ",in A pencil and watercolor drawing style"
        response_text = openai.Image.create(
            prompt=PROMPT_text,
            n=1,
            size="512x512",
            response_format="b64_json"
        )
        image_b64_text = response_text['data'][0]['b64_json']
        image_b64_text2 = b64decode(image_b64_text)
        image_data_url_text = "data:image/png;base64," + image_b64_text

        time_data = str(time.time())
        image_path = "media/diaryimages/" + str(user_id) + time_data.split('.')[0] + '.png'
        
        Image.open(BytesIO(image_b64_text2)).save(image_path)
            
        # 번역 라이브러리에 대한 이미지
        PROMPT_res = res + ",in A pencil and watercolor drawing style"
        response_res = openai.Image.create(
            prompt=PROMPT_res,
            n=1,
            size="512x512",
            response_format="b64_json"
        )
        image_b64_res = response_res['data'][0]['b64_json']
        image_b64_res2 = b64decode(image_b64_res)
        image_data_url_res = "data:image/png;base64," + image_b64_res
        
        time_data2 = str(time.time())
        image_path2 = "media/diaryimages/" + str(user_id) + time_data2.split('.')[0] + '.png'
        
        Image.open(BytesIO(image_b64_res2)).save(image_path2)

        
        context = {
            'nickname': nickname,
            'user_id': user_id,
            'date': date,
            'weather': weather,
            'emoji': emoji,
            'diary': diary,
            'image_res': image_data_url_res,
            'image_text': image_data_url_text,
            'save1':image_path,
            'save2':image_path2,
        }
        

        return render(request, 'MalLang/diarycheck.html', context)
    else:
        return render(request, 'MalLang/diarycheck.html')

def diary_save(request):
    nickname = request.session.get("nickname")
    user_id = request.session.get("user_id")

    context = {
        'nickname': nickname,
        'user_id': user_id,
    }

    if request.method == 'POST':
        if 'image_text' in request.POST:  # 첫 번째 폼에서 온 데이터
            date = request.POST.get('date')
            weather = request.POST['weather']
            emoji = request.POST['emoji']
            diary = request.POST.get('diary_text')
            image = request.POST.get('image_text')

            # DiaryEntry 모델에 데이터 저장
            entry = Diary.objects.create(
                user_id=user_id,
                diarydate=date,
                diaryweather=weather,
                diaryemoji=emoji,
                diarycontent=diary,
                image=image
                )
            if entry:
                context = {
                    'nickname': nickname,
                    'user_id': user_id,
                    'date': date,
                    'weather': weather,
                    'emoji': emoji,
                    'diary': diary,
                    'save': image
                }
                
                return render(request, 'MalLang/diarysave.html', context)
            else:
                return render(request, 'MalLang/diarysave.html', context)
            

        elif 'image_res' in request.POST:  # 두 번째 폼에서 온 데이터
            date = request.POST.get('date')
            weather = request.POST['weather']
            emoji = request.POST['emoji']
            diary = request.POST.get('diary_text')
            image = request.POST.get('image_res')

            # Entry 모델에 데이터 저장
            entry = Diary.objects.create(
                user=request.user,
                diarydate=date,
                diaryweather=weather,
                diaryemoji=emoji,
                diarycontent=diary,
                image=image
            )
            if entry:
                context = {
                    'nickname': nickname,
                    'user_id': user_id,
                    'date': date,
                    'weather': weather,
                    'emoji': emoji,
                    'diary': diary,
                    'save': image
                }
                return render(request, 'MalLang/diarysave.html', context)
            else:
                return render(request, 'MalLang/diarysave.html', context)
        
    return HttpResponse("잘못된 요청입니다.")



def board(request):
    nickname = request.session.get("nickname")
    user_id = request.session.get("user_id")
    board = Board.objects.all().order_by("-id")
    # board에 있는 객체들 id 순으로 정렬해서 다 가져옴 (- 붙여서 내림차순 정렬)

    paginator = Paginator(board, 10)
    page_num = request.GET.get("page", "1")
    # get 방식으로 받은 page 가져오고, 없으면 기본값 1

    page_obj = paginator.get_page(page_num)

    return render(request, "MalLang/board.html", {"list": page_obj, 'nickname': nickname, 'user_id': user_id})

def detail(request, id):
    board = Board.objects.get(id=id)
    image_path = board.image
    
    nickname = request.session.get("nickname")
    user_id = request.session.get("user_id")

    if user_id == board.user_id:
        notice_auth = True
    else:
        notice_auth = False
    # print(notice_auth)

    context = {
        'nickname': nickname,
        'user_id': user_id,
        'notice_auth': notice_auth,
        "dto": board,
        "image_path": image_path,
    }
    return render(request, "MalLang/detail.html", context )

def boardwrite(request):
    nickname = request.session.get("nickname")
    user_id = request.session.get("user_id")

    context = {
        'nickname': nickname,
        'user_id': user_id,
    }

    # print(user_id)

    if request.method == "GET":
        return render(request, "MalLang/boardwrite.html", context)
    elif request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        image = request.FILES.get('image')  # 이미지 업로드 부분
        date = timezone.now()


        res = Board.objects.create(user_id=user_id,
                                    nickname=nickname,
                                     title=title,
                                     content=content,
                                    image=image,
                                   date=date)

        if res:
            return redirect("board")
        else:
            return redirect("boardwrite")

    else:
        return redirect("boardwrite")

def update(request, id):
    nickname = request.session.get("nickname")
    user_id = request.session.get("user_id")
    board = Board.objects.get(id=id)
    context = {
        'nickname': nickname,
        'user_id': user_id,
        'dto':board
    }

    if request.method == "GET":
        return render(request, "MalLang/update.html", context )
    elif request.method == "POST":
        # print(request.POST)

        title = request.POST["title"]
        content = request.POST["content"]
        date = timezone.now()

        if not request.FILES.get('image_file'):
            image_path = request.POST["image"]
            image = os.path.basename(image_path)
        else:
            image = request.FILES.get('image_file')
        
        update_board = Board.objects.get(id=id)
        update_board.nickname = nickname
        update_board.title=title
        update_board.content=content
        update_board.image=image
        update_board.date=date
        
        if update_board.nickname and update_board.title and update_board.content and update_board.image and update_board.date:
            update_board.save()
            return redirect(f"/detail/{id}/")
        else:
            return redirect(f"/update/{id}/")
    else:
        return redirect("board")
    
def delete(request, id):
    result_delete = Board.objects.filter(id=id).delete()

    if result_delete[0]:
        return redirect("/board")
    else:
        return redirect(f"/detail/{id}")    
    
       
def mydiary_view(request):
    nickname = request.session.get("nickname")
    user_id = request.session.get("user_id")
    
    context = {
        'nickname': nickname,
        'user_id': user_id
    }

    diary_list = Diary.objects.filter(user_id=user_id)
    
    return render(request, "MalLang/mydiary.html", {'diary_list' : diary_list})

def diaryshow_view(request):
    nickname = request.session.get("nickname")
    user_id = request.session.get("user_id")
    
    context = {
        'nickname': nickname,
        'user_id': user_id
    }

    if request.method == 'POST':
        date = request.POST.get('date')
        weather = request.POST.get('weather')
        emoji = request.POST.get('emoji')
        diary = request.POST.get('diary_text')
        image = request.POST.get('image_text')
        
    context = {
        'nickname': nickname,
        'user_id': user_id,
        'date':date,
        'weather':weather,
        'emoji':emoji,
        'diary':diary,
        'image':image
        
    }
    
    return render(request, "MalLang/diaryshow.html", context)


# your_localhost need
def search_engine(request):
    es = Elasticsearch(
    hosts=['http://localhost:9200'],
    basic_auth=('elastic', 'mallang0000')
    )
    
    user_id = request.session.get("user_id")

    diary_list = Diary.objects.filter(user_id=user_id)

    diary = serializers.serialize('json', diary_list)
    
    if es.indices.exists(index='dictionary'):
        pass
    else:
        es.indices.create(
            index='dictionary',
            body={
                "settings": {
                    "index": {
                        "analysis": {
                            "analyzer": {
                                "my_analyzer": {
                                    "type": "custom",
                                    "tokenizer": "nori_tokenizer"
                                }
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "diarydate": {
                            "type": "date"
                        },
                        "image": {
                            "type": "text"
                        },
                        "diarycontent": {
                            "type": "text",
                            "analyzer": "my_analyzer"
                        }
                    }
                }
            }
        )
    
    
    body = ""
    for i in diary:
        body = body + json.dumps({"index": {"_index": "dictionary"}}) + '\n'
        body = body + json.dumps(i, ensure_ascii=False) + '\n'
    
    es.bulk(body=body)

    return redirect('/search_view')
class SearchView(APIView):

    # def get(self, request):
    #     es = Elasticsearch(
    #         [
    #             {'host':'localhost', 'port':9200, 'scheme':"http"}
    #         ])
    def get(self, request):
        es = Elasticsearch(
            hosts=[{'host':'localhost', 'port':9200, 'scheme':"http"}],
            http_auth=('elastic', 'mallang0000')
        )

        # 검색어
        search_word = request.query_params.get('search')

        if not search_word:
            return render(request, 'MalLang/search.html')
        # print(es.info())
        docs = es.search(
                         body={
                             "query": {
                                 "multi_match": {
                                     "query": search_word,
                                     "fields": ["diarycontent"]
                                 }
                             }
                         })
        # print(docs)
        # data_list = docs['hits']
        # print([hit['_source'] for hit in docs['hits']['hits']])
        contents = [hit['_source'] for hit in docs['hits']['hits']]
        for diary in contents:
            diary['diarydate'] = diary['diarydate'].split('T')[0]
        # print(contents)

        # return Response(data_list)
        # return render(request, 'search_results.html', {'search_results': data_list})
        return render(request, 'MalLang/search_results.html', {'search_results': contents})


import urllib.parse
import urllib.request
from django.http import HttpResponse

def tts_diary(request):
    # 사용자가 쓴 일기 내용을 가져옵니다. 
    # 예를 들어, Diary 모델에서 최근 일기를 가져오는 경우입니다.
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        diary_content = data.get('content', '')
        # print(diary_content)

        client_id = tts_diary_client_id
        client_secret = tts_diary_secret_key
        encText = urllib.parse.quote(diary_content)
        speaker = urllib.parse.quote("nhajun")
        data = f"volume=0&speed=0&pitch=0&speaker={speaker}&format=mp3&text={encText}"
        url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        request.add_header("X-NCP-APIGW-API-KEY", client_secret)
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read()
            # 직접 응답으로 MP3 데이터를 전달합니다.
            return HttpResponse(response_body, content_type="audio/mpeg")
        else:
            return HttpResponse("TTS 오류 발생", status=500)
    else:
        return HttpResponse("Invalid Request", status=400)