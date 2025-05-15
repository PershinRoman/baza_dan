from hh_api import HHApi
from db_manager import DBManager


def main():
    """
    Основная функция программы.
    Получает данные о компаниях и их вакансиях через апи ххру
    и заполняет бд полученными данными
    Выводит количество вакансий у каждой компании на экран
    :return:
    """

    db_manager = DBManager(db_name='table_hh_ru', user='roman', password='159')

    db_manager.create_tables()

    api = HHApi()

    company_ids = ['12345', '67890']  # !!!!!


for company in api.get_companies(company_ids):
    company_id = db_manager.insert_company(company['name'])

    for vacancy in api.get_vacancies(company['id']):
        db_manager.insert_vacancy['name'], vacancy.get('salary_from'), vacancy.get('salary_to'), vacancy[
            'alternate_url'], company_id()

    print(db_manager.get_companies_and_vacancies_count())

    db_manager.close()