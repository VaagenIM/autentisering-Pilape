# Flask Autentiserings Eksempel

## Hvordan kjøre:

```python
pip install -r requirements.txt
python src/run.py
```

Besøk http://localhost:5000

## Deploy
Lag en fil som heter .env:
```env
FLASK_SECRET_KEY="SKRIV NOE HER"
PEPPER="SKRIV NOE HER"
```

> [!WARNING]
> Hvis du ikke lager env filen bruker appen backup verdiene lagret direkte i koden.

Filstrukturen skal inneholde disse filene:
```
src/
.env
compose.yml
Dockerfile
requirements.txt
```

Deretter kjører du:
```bash
docker compose up -d
```