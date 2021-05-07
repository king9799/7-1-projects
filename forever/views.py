from django.shortcuts import render, redirect
from forever.models import *
from django.contrib.auth.decorators import login_required
import segno
import urllib.request
import json
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
import youtube_dl
from django.contrib import messages
from googletrans import Translator
import pyttsx3
from django.contrib.auth import authenticate, login, logout
import speech_recognition as sr

# Create your views here.


@login_required(redirect_field_name='login')
def index(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'user': request.user})


def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            users = User.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password1']
            )
            users.save()
            print('success')
            return redirect('/login')
        else:
            return redirect('/register')
    else:
        return render(request, 'register.html')


def logout_request(request):
    logout(request)
    return redirect('/login')


@login_required(redirect_field_name='login')
def news(request):
    if request.method == 'POST':
        news = request.POST['news']
        print(news)
        try:
            source = urllib.request.urlopen('https://newsapi.org/v2/everything?q='+ str(news) +'&from=2021&sortBy=popularity&apiKey=ea4c5fca574841a98072886a861bc189').read()
            list_of_data = json.loads(source)
            print(list_of_data['articles'])
            return render(request, 'news.html', {'data': list_of_data['articles']})

        except:
            return redirect('/news')
    else:
        return render(request, 'news.html')


def text_speech(self):
    king = pyttsx3.init()
    king.say(self)
    king.runAndWait()


@login_required(redirect_field_name='login')
def texttospech(request):
    if request.method == 'POST':
        if 'stt' in request.POST:
            messages.success(request, "Are you Talking...")
            ear = sr.Recognizer()
            with sr.Microphone() as sourse:
                audio = ear.listen(sourse)
                try:
                    text = ear.recognize_google(audio)
                    if text == ('hi' or 'hello'):
                        text_speech('welcome my site')
                        return render(request, 'texttospech.html', {'text': text})
                    elif text == ('who are you' or 'who'):
                        text_speech('I am KING')
                        return render(request, 'texttospech.html', {'text': text})
                    else:
                        return render(request, 'texttospech.html', {'text': text})
                except:
                    print("i didn't get that...")
        else:
            king = pyttsx3.init()
            king.say(request.POST['tts'])
            king.runAndWait()
            return render(request, 'texttospech.html')
    return render(request, 'texttospech.html')


@login_required(redirect_field_name='login')
def translate(request):
    if request.method == 'POST':
        translate = Translator()
        result = translate.translate(request.POST['text'], dest='uz')
        print(result)
        return render(request, 'translate.html', {'result': result})
    return render(request, 'translate.html')


@login_required(redirect_field_name='login')
def qrcode(request):
    if request.method == 'POST':
        img = segno.make_qr(request.POST['address'])
        img.save('static/qrcode.png', scale=40)
        return redirect('/qrcode')
    return render(request, 'qrcode.html')


@login_required(redirect_field_name='login')
def todoadd(request):
    todos = Todo.objects.filter(step__contains='one')
    todod = Todo.objects.filter(step__contains='two')
    todof = Todo.objects.filter(step__contains='three')
    history = Todo.objects.filter(step__contains='four', )
    if request.method == 'POST':
        todo = Todo.objects.create(
            title=request.POST['title'],
            description=request.POST['description']
        )
        todo.save()
    return render(request, 'add.html', {'todos': todos, 'todod': todod, 'todof': todof, 'todoh': history})


def delete(request, id):
    todo = Todo.objects.get(id=id)
    todo.delete()
    return redirect('/todo')


@login_required(redirect_field_name='login')
def doing(request, id):
    todo = Todo.objects.get(id=id)
    todo.step = 'two'
    todo.save()
    return redirect('/todo')


@login_required(redirect_field_name='login')
def finish(request, id):
    todo = Todo.objects.get(id=id)
    todo.step = 'three'
    todo.save()
    return redirect('/todo')


@login_required(redirect_field_name='login')
def history(request, id):
    todo = Todo.objects.get(id=id)
    todo.step = 'four'
    todo.save()
    return redirect('/todo')


@login_required(redirect_field_name='login')
def weather(request):
    if request.method == 'POST':
        city = request.POST['city']
        a = str(city)
        city = ''
        if 1 != len(a.split()):
            for i in a.split():
                city += i + '%20'
        else:
            city = a

        try:
            source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&appid=335aa256ed01c1518060e73e36a436cd').read()
            list_of_data = json.loads(source)
            data = {
                "name": str(list_of_data['name']),
                "country_code": str(list_of_data['sys']['country']),
                "coordinate": str(list_of_data['coord']['lon']) + ', '
                + str(list_of_data['coord']['lat']),
                "temp": str(list_of_data['main']['temp']) + ' °C',
                "pressure": str(list_of_data['main']['pressure']),
                "humidity": str(list_of_data['main']['humidity']),
                'main': str(list_of_data['weather'][0]['main']),
                'description': str(list_of_data['weather'][0]['description']),
                'icon': list_of_data['weather'][0]['icon'],
            }
        except:
            return HttpResponseRedirect('/weather',)

    else:
        data = {}

    return render(request, "weather.html", data)


@login_required(redirect_field_name='login')
def download_video(request):
    if request.method == 'POST':
        try:
            video_url = request.POST['url']
            if video_url:
                ydl_opts = {'outtmp1': 'D:/'}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                messages.success(request, 'Video Downloaded.')
                return redirect('download')
            else:
                messages.warning(request, 'Please Enter Video URL')
                return redirect('download')
        except:
            messages.error(request, 'VIDEO URL NOT POUND')
            return redirect('download')
    return render(request, 'download.html')