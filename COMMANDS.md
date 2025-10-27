# PDF Monitor - Команды управления

## 📦 Установка зависимостей

```bash
pip3 install requests watchdog
```

## 🚀 Запуск скрипта

### ▶️ Запуск в фоновом режиме (рекомендуется)
```bash
nohup python3 ~/pdf_monitor_MacAir.py > /tmp/pdfmonitor.out 2>&1 &
```

### 🖥️ Запуск в терминале (для тестирования)
```bash
python3 ~/pdf_monitor_MacAir.py
```

## 🛑 Остановка скрипта

```bash
pkill -f pdf_monitor_MacAir.py
```

## 🔄 Перезапуск скрипта

```bash
pkill -f pdf_monitor_MacAir.py && nohup python3 ~/pdf_monitor_MacAir.py > /tmp/pdfmonitor.out 2>&1 &
```

## 📊 Проверка статуса

### ✅ Проверить работает ли процесс
```bash
ps aux | grep pdf_monitor
```

### 📝 Посмотреть логи (последние 20 строк)
```bash
tail -20 /tmp/pdfmonitor.out
```

### 👀 Мониторинг логов в реальном времени
```bash
tail -f /tmp/pdfmonitor.out
```

### ⚠️ Посмотреть ошибки
```bash
tail -20 /tmp/pdfmonitor.err
```

## 🎯 Удобные alias (добавить в ~/.zshrc)

### Создать alias для быстрого запуска
```bash
echo 'alias pdfmon="python3 ~/pdf_monitor_MacAir.py"' >> ~/.zshrc
source ~/.zshrc
```

### Создать alias для запуска в фоне
```bash
echo 'alias pdfmon-start="nohup python3 ~/pdf_monitor_MacAir.py > /tmp/pdfmonitor.out 2>&1 &"' >> ~/.zshrc
source ~/.zshrc
```

### Создать alias для остановки
```bash
echo 'alias pdfmon-stop="pkill -f pdf_monitor_MacAir.py"' >> ~/.zshrc
source ~/.zshrc
```

### Создать alias для перезапуска
```bash
echo 'alias pdfmon-restart="pkill -f pdf_monitor_MacAir.py && nohup python3 ~/pdf_monitor_MacAir.py > /tmp/pdfmonitor.out 2>&1 &"' >> ~/.zshrc
source ~/.zshrc
```

### Создать alias для просмотра логов
```bash
echo 'alias pdfmon-logs="tail -f /tmp/pdfmonitor.out"' >> ~/.zshrc
source ~/.zshrc
```

После добавления всех alias, команды будут:
- `pdfmon-start` - запустить в фоне
- `pdfmon-stop` - остановить
- `pdfmon-restart` - перезапустить
- `pdfmon-logs` - смотреть логи
- `pdfmon` - запустить в терминале

## 📂 Путь к папке мониторинга

```
/Users/alex/Documents/Mega/С Т Р А Х О В А Н И Е/Т А С/2025/Оформлено
```

## 📄 Расположение файлов

- **Скрипт:** `~/pdf_monitor_MacAir.py`
- **Логи:** `/tmp/pdfmonitor.out`
- **Ошибки:** `/tmp/pdfmonitor.err`
- **История отправленных:** `~/sent_files.json`

## ⚙️ Настройки в скрипте

Для изменения настроек отредактируйте файл `~/pdf_monitor_MacAir.py` (строки 121-123):

```python
FOLDER_PATH = "/Users/alex/Documents/Mega/..."  # Папка для мониторинга
BOT_TOKEN = "ваш_токен_бота"                    # Токен Telegram бота
CHAT_ID = "ваш_chat_id"                         # ID чата
```

## ⚡ Быстрый старт

1. Установите зависимости:
   ```bash
   pip3 install requests watchdog
   ```

2. Запустите в фоне:
   ```bash
   nohup python3 ~/pdf_monitor_MacAir.py > /tmp/pdfmonitor.out 2>&1 &
   ```

3. Проверьте что работает:
   ```bash
   ps aux | grep pdf_monitor
   tail -f /tmp/pdfmonitor.out
   ```

## 🔧 Решение проблем

### Скрипт не запускается
```bash
# Проверьте права на выполнение
chmod +x ~/pdf_monitor_MacAir.py

# Проверьте установлены ли зависимости
pip3 list | grep -E "requests|watchdog"
```

### Не видит новые файлы
```bash
# Перезапустите скрипт
pkill -f pdf_monitor_MacAir.py
nohup python3 ~/pdf_monitor_MacAir.py > /tmp/pdfmonitor.out 2>&1 &
```

### Ошибки отправки в Telegram
```bash
# Проверьте логи ошибок
cat /tmp/pdfmonitor.err

# Проверьте токен и chat_id в скрипте
grep -E "BOT_TOKEN|CHAT_ID" ~/pdf_monitor_MacAir.py
```

## ℹ️ Важная информация

- ✅ Процесс работает в фоне даже после закрытия терминала
- ✅ Переживает сон/пробуждение Mac
- ❌ Останавливается после перезагрузки (нужно запускать вручную)
- 📱 Отправляет PDF файлы в Telegram автоматически
- 🔍 Мониторит папку и все подпапки рекурсивно
- 💾 Помнит отправленные файлы (не отправляет повторно)
