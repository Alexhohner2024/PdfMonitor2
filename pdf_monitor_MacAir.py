import os
import time
import json
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

class PDFHandler(FileSystemEventHandler):
    def __init__(self, bot_token, chat_id, sent_files_path, base_folder):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.sent_files_path = sent_files_path
        self.base_folder = base_folder
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        
        # Загружаем список отправленных файлов
        self.sent_files = self.load_sent_files()
    
    def load_sent_files(self):
        """Загружает список уже отправленных файлов"""
        if os.path.exists(self.sent_files_path):
            with open(self.sent_files_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_sent_files(self):
        """Сохраняет список отправленных файлов"""
        with open(self.sent_files_path, 'w', encoding='utf-8') as f:
            json.dump(self.sent_files, f, ensure_ascii=False, indent=2)
    
    def on_created(self, event):
        """Вызывается при создании нового файла"""
        if event.is_directory:
            return
        
        file_path = event.src_path
        
        # Ігноруємо .download папки (для Safari)
        if '.download' in file_path:
            return
        
        # Проверяем, что это PDF файл
        if not file_path.lower().endswith('.pdf'):
            return
        
        # Ждем, пока файл полностью скачается
        self.wait_for_file_ready(file_path)
        
        # Проверяем, не отправляли ли уже этот файл
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_key = f"{file_name}_{file_size}"
        
        if file_key in self.sent_files:
            print(f"Файл {file_name} уже был отправлен ранее")
            return
        
        # Отправляем файл
        relative_path = os.path.relpath(file_path, self.base_folder)
        print(f"Найден новый PDF: {relative_path}")
        success = self.send_pdf_to_bot(file_path)
        
        if success:
            self.sent_files.append(file_key)
            self.save_sent_files()
            print(f"✅ Файл {file_name} успешно отправлен")
        else:
            print(f"❌ Ошибка отправки файла {file_name}")
    
    def wait_for_file_ready(self, file_path, timeout=30):
        """Ждет, пока файл полностью скачается"""
        start_time = time.time()
        last_size = 0
        
        while time.time() - start_time < timeout:
            try:
                current_size = os.path.getsize(file_path)
                if current_size == last_size and current_size > 0:
                    # Размер не изменился - файл готов
                    time.sleep(1)  # Дополнительная пауза
                    return True
                last_size = current_size
                time.sleep(2)
            except OSError:
                # Файл еще не готов
                time.sleep(1)
        
        return True  # Продолжаем даже если не дождались
    
    def send_pdf_to_bot(self, file_path):
        """Отправляет PDF файл в Telegram бот"""
        try:
            url = f"{self.base_url}/sendDocument"
            
            file_name = os.path.basename(file_path)
            
            with open(file_path, 'rb') as pdf_file:
                files = {
                    'document': (file_name, pdf_file, 'application/pdf')
                }
                data = {
                    'chat_id': self.chat_id
                }
                
                response = requests.post(url, files=files, data=data, timeout=60)
                result = response.json()
                
                if result.get('ok'):
                    return True
                else:
                    print(f"Ошибка Telegram API: {result.get('description', 'Неизвестная ошибка')}")
                    return False
                    
        except Exception as e:
            print(f"Ошибка отправки: {e}")
            return False

def main():
    # НАСТРОЙКИ - ИЗМЕНИТЕ ЭТИ ЗНАЧЕНИЯ
    FOLDER_PATH = "/Users/alex/Documents/Mega/С Т Р А Х О В А Н И Е/Т А С/2025/Оформлено"  # Путь к папке для мониторинга
    BOT_TOKEN = "8053923426:AAEL3QnXjyqgdV87NIvETVtMfomiLC23ITg"  # Токен вашего бота
    CHAT_ID = "-1002508092259"                             # ID чата с ботом
    
    # Файл для хранения списка отправленных файлов
    sent_files_path = "sent_files.json"
    
    # Проверяем настройки
    if not os.path.exists(FOLDER_PATH):
        print(f"❌ Папка не найдена: {FOLDER_PATH}")
        return
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Укажите токен бота в переменной BOT_TOKEN")
        return
    
    if CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("❌ Укажите Chat ID в переменной CHAT_ID")
        return
    
    # Создаем обработчик событий
    event_handler = PDFHandler(BOT_TOKEN, CHAT_ID, sent_files_path, FOLDER_PATH)
    
    # Создаем наблюдатель
    observer = Observer()
    observer.schedule(event_handler, FOLDER_PATH, recursive=True)
    
    # Запускаем мониторинг
    observer.start()
    print(f"🔍 Мониторинг папки (включая подпапки): {FOLDER_PATH}")
    print("📱 Отправка в Telegram бот настроена")
    print("✋ Нажмите Ctrl+C для остановки")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Мониторинг остановлен")
    
    observer.join()

if __name__ == "__main__":
    main()