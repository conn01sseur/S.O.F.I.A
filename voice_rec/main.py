import vosk
import pyaudio
import json
import requests

# Ваш API-ключ OpenAI
API_KEY = 'sk-uvwxijklmnop1234uvwxijklmnop1234uvwxijkl'  # Замените на ваш реальный API-ключ

# Инициализация модели Vosk
model = vosk.Model("vosk-model-ru-0.42")  # Укажите путь к модели
recognizer = vosk.KaldiRecognizer(model, 16000)

# Настройка аудиопотока
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
stream.start_stream()

print("Скажите что-нибудь:")

while True:
    data = stream.read(4000, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        result_json = json.loads(result)  # Разбираем строку JSON
        text = result_json.get('text', '')  # Извлекаем текст
        print("Вы сказали:", text)

        # Проверяем, если текст не пустой
        if text:
            # Отправляем текст в ChatGPT
            url = 'https://api.openai.com/v1/chat/completions'
            headers = {
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json',
            }
            data = {
                'model': 'gpt-3.5-turbo',  # Вы можете использовать gpt-4, если у вас есть доступ
                'messages': [
                    {'role': 'user', 'content': text}
                ],
            }

            # Отправка POST-запроса
            response = requests.post(url, headers=headers, json=data)

            # Проверка статуса ответа
            if response.status_code == 200:
                response_data = response.json()
                chatgpt_response = response_data['choices'][0]['message']['content']
                print("Ответ ChatGPT:", chatgpt_response)
            else:
                print("Ошибка при обращении к API OpenAI:", response.status_code, response.text)
