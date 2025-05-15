import psycopg2
from hh_api import search_companies, get_companies, get_vacancies_for_company
from db_manager import DBManager


def main():
    # Настройки подключения к базе данных
    db_params = {
        'db_name': 'baza_dan',
        'user': 'postgres',
        'password': '159',
        'host': 'localhost',
        'port': 5432
    }

    db_manager = DBManager(**db_params)

    # Создаем таблицы
    db_manager.create_tables()

    # Получаем список компаний
    company_ids = search_companies()

    print("Загружаем данные о компаниях и вакансиях...")

    for comp_id in company_ids:
        # Получаем информацию о компании
        comp_info_response = get_companies([comp_id])

        if comp_info_response:
            company_info = comp_info_response[0]

            # Извлекаем нужные поля (пример)
            company_name = company_info.get('name')
            company_id = company_info.get('id')
            description = company_info.get('description', '')
            url = company_info.get('alternate_url', '')

            # Сохраняем компанию в базу данных
            db_manager.insert_company(company_id, company_name, description, url)

            # Получаем вакансии для компании
            vacancies = get_vacancies_for_company(comp_id)

            for vacancy in vacancies:
                vacancy_id = vacancy.get('id')
                vacancy_name = vacancy.get('name')
                salary_from = vacancy.get('salary', {}).get('from')
                salary_to = vacancy.get('salary', {}).get('to')
                currency = vacancy.get('salary', {}).get('currency')
                employer_name = vacancy.get('employer', {}).get('name')
                published_at = vacancy.get('published_at')
                url_vacancy = vacancy.get('alternate_url')

                # Сохраняем вакансию в базу данных
                db_manager.insert_vacancy(
                    vacancy_id,
                    vacancy_name,
                    salary_from,
                    salary_to,
                    currency,
                    employer_name,
                    published_at,
                    url_vacancy,
                    company_id  # связываем вакансию с компанией
                )
        else:
            print(f"Не удалось получить информацию о компании с ID {comp_id}")


# Вызов функции при запуске скрипта
if __name__ == "__main__":
    main()
