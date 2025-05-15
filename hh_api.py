import requests
from typing import List, Dict, Optional


class HHApi:
    """Класс для взаимодействия с апи хх ру"""

    __slots__ = ()

    def __init__(self) -> None:
        """Инициализация экземпляра"""
        pass

    def _get_response(self, url: str, params: Optional[Dict] = None) -> Dict:
        """Привватный метод для выполнения гет запроса к апи ххру"""
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise RuntimeError(f"API req failed with status {response.status_code}")
        return response.json()

    BASE_URL = 'http://api.hh.ru'

    def get_companies(self, company_ids):
        """Получает информацию о компаниях по их айди"""
        companies = []
        for company_id in company_ids:
            response = requests.get(f"{self.BASE_URL}/employers/{company_id}")
            if response.status_code == 200:
                companies.append(response.json())
        return companies

    def get_vacancies(self, company_id):
        """Получает список вакансий для заданной компании по ее ID"""
        vacancies = []
        response = requests.get('{self.BASE_URL}/vacancies?employer_id={company_id}')
        if response.status_code == 200:
            vacancies = response.json().get('items', [])
        return vacancies
