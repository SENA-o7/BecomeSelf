# BECOME SELF

Hedefleri, alışkanlıkları ve günlük eylemleri birbirine bağlayan; kullanıcının gerçek davranışına göre planı yeniden düzenleyen bir kişisel gelişim sistemi.

## Yapı

```
backend/   FastAPI sunucusu (Python) — planlama kuralları burada
mobile/    Flutter uygulaması (ileride)
docker-compose.yml   PostgreSQL veritabanı
```

## Backend'i çalıştırma

```powershell
# 1. Veritabanını aç (Docker Desktop açık olmalı)
docker compose up -d

# 2. Backend klasörüne geç ve sanal ortamı etkinleştir
cd backend
.\.venv\Scripts\Activate.ps1

# 3. Sunucuyu başlat
fastapi dev app/main.py
```

Ardından tarayıcıda http://127.0.0.1:8000/docs adresini aç.

İlk kurulumda (sanal ortam yoksa):

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
copy .env.example .env
```

## Testler

```powershell
cd backend
pytest -v
```

## Veritabanını kapatma

```powershell
docker compose down        # kapatır, veriler kalır
docker compose down -v     # kapatır ve tüm verileri siler
```
