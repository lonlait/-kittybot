# Деплой на PythonAnywhere 🚀

## Пошаговая инструкция

### 1. Подготовка проекта

1. Загрузите все файлы проекта на GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/kittybot.git
   git push -u origin main
   ```

### 2. Настройка PythonAnywhere

1. **Зарегистрируйтесь на PythonAnywhere** (https://www.pythonanywhere.com/)
2. **Войдите в аккаунт** и перейдите в раздел "Web"

### 3. Создание веб-приложения

1. **Нажмите "Add a new web app"**
2. **Выберите "Flask"** в качестве фреймворка
3. **Выберите Python 3.9** (или новее)
4. **Укажите путь к проекту**: `/home/yourusername/kittybot`

### 4. Загрузка кода

1. **Откройте Bash консоль** на PythonAnywhere
2. **Клонируйте репозиторий**:
   ```bash
   cd /home/yourusername
   git clone https://github.com/yourusername/kittybot.git
   cd kittybot
   ```

### 5. Установка зависимостей

1. **Создайте виртуальное окружение**:
   ```bash
   python3.9 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### 6. Настройка переменных окружения

1. **Создайте файл `.env`**:
   ```bash
   echo "TOKEN=8080191792:AAGsMYDNl4qkCA6DrV--kxap-DKYFS4Ndic" > .env
   echo "PYTHONANYWHERE_SITE=yourusername.pythonanywhere.com" >> .env
   ```

### 7. Настройка WSGI файла

1. **Откройте WSGI файл** в разделе "Web" → "Code" → "WSGI configuration file"
2. **Замените содержимое** на:

```python
import sys
import os

# Добавляем путь к проекту
path = '/home/yourusername/kittybot'
if path not in sys.path:
    sys.path.append(path)

# Активируем виртуальное окружение
activate_this = '/home/yourusername/kittybot/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Импортируем приложение
from app import app as application
```

### 8. Настройка веб-приложения

1. **В разделе "Web"** → **"Code"**:
   - **Source code**: `/home/yourusername/kittybot`
   - **Working directory**: `/home/yourusername/kittybot`
   - **WSGI configuration file**: оставьте как есть

2. **В разделе "Web"** → **"Files"**:
   - Убедитесь, что все файлы загружены

### 9. Установка webhook

1. **Перейдите на ваш сайт**: `https://yourusername.pythonanywhere.com/set_webhook`
2. **Должно появиться сообщение**: "Webhook установлен: https://yourusername.pythonanywhere.com/webhook"

### 10. Перезапуск приложения

1. **Нажмите "Reload"** в разделе "Web"
2. **Проверьте логи** в разделе "Web" → "Log files" → "Error log"

## Проверка работы

1. **Откройте сайт**: `https://yourusername.pythonanywhere.com`
2. **Должна появиться страница** с информацией о боте
3. **Найдите бота в Telegram**: `@CatSuperpositionBot`
4. **Отправьте команду** `/start`

## Устранение неполадок

### Ошибка "Module not found"
- Убедитесь, что виртуальное окружение активировано в WSGI файле
- Проверьте, что все зависимости установлены

### Ошибка "Token not found"
- Проверьте файл `.env` в корне проекта
- Убедитесь, что токен правильный

### Бот не отвечает
- Проверьте webhook: `https://yourusername.pythonanywhere.com/set_webhook`
- Посмотрите логи ошибок в разделе "Web"

### Ошибка 500
- Проверьте логи в разделе "Web" → "Log files"
- Убедитесь, что все импорты корректны

## Полезные команды

```bash
# Проверка статуса приложения
curl https://yourusername.pythonanywhere.com

# Установка webhook
curl https://yourusername.pythonanywhere.com/set_webhook

# Удаление webhook
curl https://yourusername.pythonanywhere.com/remove_webhook

# Просмотр логов
tail -f /var/log/yourusername.pythonanywhere.com.error.log
```

## Мониторинг

- **Логи ошибок**: Web → Log files → Error log
- **Логи доступа**: Web → Log files → Access log
- **Статус приложения**: Web → Status

## Обновление бота

1. **Загрузите изменения на GitHub**
2. **В PythonAnywhere**:
   ```bash
   cd /home/yourusername/kittybot
   git pull
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Перезапустите приложение** (Reload)

## Важные замечания

- **Бесплатный аккаунт** имеет ограничения на CPU время
- **Бот будет работать только при активных запросах**
- **Для постоянной работы** рассмотрите платные планы
- **Регулярно проверяйте логи** на наличие ошибок 