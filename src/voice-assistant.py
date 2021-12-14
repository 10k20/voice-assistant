# Голосовой ассистент КЕША 1.0 BETA
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import subprocess
import random
import signal

# настройки
opts = {
    "alias": ('венера'),
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси'),
    "cmds": {
        "music": ('включи музыку', 'музыка'),
        "stop music": ('пауза', 'останови музыку', 'поставь на паузу', 'поставь музыку на паузу'),
        "ctime": ('текущее время','сейчас времени','который час', 'время'),
        "stupid": ('расскажи анекдот','рассмеши меня','ты знаешь анекдоты', 'анекдот', 'шутка')
    }
}

# функции
def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Распознано: " + voice)
    
        if voice.startswith(opts["alias"]):
            # обращаются к Венере
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()
            
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
            
            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    
    return RC

def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    
    elif cmd == 'music':
        # воспроизвести радио
        mylist = os.listdir('./audio')
        audio_file = "./audio/" + random.choice(mylist)
        return_code = subprocess.call(["afplay", audio_file])

    elif cmd == 'stop music':
      pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
      os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Send the signal to all the process groups
    
    elif cmd == 'stupid':
        # рассказать анекдот
        speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")
    
    else:
        print('Команда не распознана, повторите!')

# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index = 0)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

speak("Добрый день, пользователь")
speak("Меня зовут Венера. Я Ваш голсовой помощник")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # infinity loop