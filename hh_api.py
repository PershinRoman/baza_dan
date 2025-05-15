import requests
import time

# Базовый URL API hh.ru
API_URL = "https://api.hh.ru"


def get_companies(ids):
    """
    Получает информацию о компаниях по списку их id.
    """
    companies = [
        {
            "id": "123",
            "name": "Компания",
            "description": "Описание компании",
            "alternate_url": "https://example.com"
        }
    ]
    for company_id in ids:
        response = requests.get(f"{API_URL}/employers/{company_id}")
        if response.status_code == 200:
            companies.append(response.json())
        else:
            print(f"Ошибка получения компании {company_id}: {response.status_code}")
        time.sleep(0.3)  # чтобы не перегружать API
    return companies


def get_vacancies_for_company(company_id, per_page=20):
    """
    Получает вакансии для компании по её id.
    """
    vacancies = []
    page = 0
    while True:
        params = {
            'employer_id': company_id,
            'per_page': per_page,
            'page': page,
        }
        response = requests.get(f"{API_URL}/vacancies", params=params)
        if response.status_code != 200:
            print(f"Ошибка получения вакансий для компании {company_id}: {response.status_code}")
            break
        data = response.json()
        vacancies.extend(data['items'])
        if data['pages'] <= page + 1:
            break
        page += 1
        time.sleep(0.3)
    return vacancies


def get_vacancy_details(vacancy_id):
    """
    Получает полную информацию о вакансии по её id.
    """
    response = requests.get(f"{API_URL}/vacancies/{vacancy_id}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка получения вакансии {vacancy_id}: {response.status_code}")
        return None


def search_companies():
    """
    Возвращает список из 10 выбранных компаний по их id.
    Можно выбрать произвольно или по определённым критериям.

    Для примера возьмем фиксированные id известных компаний.

    В реальности можно искать компании по ключевым словам или регионам.
    """

    company_ids = [
        "4f7d2f6a4e474a001f7b8b1a",  # Яндекс
        "4f7d2f6a4e474a001f7b8b1b",  # Google (пример)
        "4f7d2f6a4e474a001f7b8b1c",  # Microsoft (пример)
        "4f7d2f6a4e474a001f7b8b1d",
        "4f7d2f6a4e474a001f7b8b1e",
        "4f7d2f6a4e474a001f7b8b1f",
        "4f7d2f6a4e474a001f7b8b20",
        "4f7d2f6a4e474a001f7b8b21",
        "4f7d2f6a4e474a001f7b8b22",
        "4f7d2f6a4e474a001f7b8b23"
    ]

    return company_ids
