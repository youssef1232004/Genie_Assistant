import requests
import json
import sys
import time
import threading

API_KEY = "Add_Your_API_Key"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + API_KEY

text = ""

if len(sys.argv) > 1:
    text = "Refuse to answer if the question is not about bash terminal: " + sys.argv[1]

payload = {
    "contents": [
        {
            "parts": [
                {"text": text + "provide a brief listed answer explain the options with  examples for each option"}
            ]
        }
    ]
}

headers = {
    "Content-Type": "application/json"
}

print("\n")

def loading_animation(stop_event):
    animation_frames = ['|', '/', '-', '\\']
    while not stop_event.is_set():
        for frame in animation_frames:
            sys.stdout.write('\rProcessing your request......' + frame)
            sys.stdout.flush()
            time.sleep(0.1)

stop_event = threading.Event()

try:
    t = threading.Thread(target=loading_animation, args=(stop_event,))
    t.start()

    response = requests.post(URL, json=payload, headers=headers)
    response.raise_for_status()

    stop_event.set()
    t.join()

    data = response.json().get('candidates')[0].get('content').get('parts')[0].get('text')

    sys.stdout.write('\r' + ' ' * 50 + '\r')

    if "answer" not in data.lower(): 
        print(f"\n {data}\n")
        print("\n🎉 Response received successfully!\n")
    else:
        print("\nSorry😞, I answer questions about terminal bash only\n")

     

except requests.exceptions.ConnectionError as conn_err:
    stop_event.set()
    t.join()
    print("\n❌ Connection error occurred:")
    print(f"{conn_err}")
except Exception as e:
    stop_event.set()
    t.join()
    print("\n❌ An unexpected error occurred:")
    print(f"{e}")
