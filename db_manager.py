import psycopg2


class DBManager:
    def __init__(self, db_name, user, password, host='localhost', port=5432):
        self.connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()

    def create_tables(self):
        # Создаем таблицы для компаний и вакансий
        create_companies_table = """
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            company_id VARCHAR(50) UNIQUE NOT NULL,
            name VARCHAR(255),
            description TEXT,
            url TEXT
        );
        """

        create_vacancies_table = """
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            vacancy_id VARCHAR(50) UNIQUE NOT NULL,
            name VARCHAR(255),
            salary_from NUMERIC,
            salary_to NUMERIC,
            currency VARCHAR(10),
            employer_name VARCHAR(255),
            published_at TIMESTAMP,
            url TEXT,
            company_id VARCHAR(50) REFERENCES companies(company_id)
        );
        """

        self.cursor.execute(create_companies_table)
        self.cursor.execute(create_vacancies_table)
        self.connection.commit()

    def insert_company(self, company_id, name, description, url):
        insert_query = """
        INSERT INTO companies (company_id, name, description, url)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (company_id) DO NOTHING;
        """
        self.cursor.execute(insert_query, (company_id, name, description, url))
        self.connection.commit()

    def insert_vacancy(self, vacancy_id, name, salary_from, salary_to, currency,
                       employer_name, published_at, url, company_id):
        insert_query = """
        INSERT INTO vacancies (vacancy_id, name, salary_from, salary_to, currency,
                               employer_name, published_at, url, company_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (vacancy_id) DO NOTHING;
        """
        self.cursor.execute(insert_query,
                            (vacancy_id, name, salary_from or None,
                             salary_to or None, currency,
                             employer_name, published_at,
                             url, company_id))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
