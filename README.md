# FastAPI test backend

Простой тестовый бэкенд на FastAPI, который возвращает текущее время сервера.

## Запуск

1. Создайте виртуальное окружение:

```bash
python -m venv .venv
```

2. Активируйте виртуальное окружение:

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Запустите сервер:

```bash
uvicorn app.main:app --reload
```

5. Откройте endpoint:

`GET /time`  
Пример: `http://127.0.0.1:8000/time`
