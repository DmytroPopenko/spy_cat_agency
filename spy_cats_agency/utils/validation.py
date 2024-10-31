import requests

BREED_API = "https://api.thecatapi.com/v1/breeds"

def validate_cat_breed(breed: str) -> bool:
    try:
        response = requests.get(BREED_API)
        response.raise_for_status()  # викличе виключення, якщо статус-код не 200

        breeds = response.json()
        print(breed)
        return any(b['name'].lower() == breed.lower() for b in breeds)
    except requests.RequestException:
        # Випадок, коли запит не вдався
        return False