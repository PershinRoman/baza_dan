import psycopg2
from psycopg2 import sql


class DBManager:
    def __init__(self, db_name, user, password, host='localhost', port=5432):
        self.connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.connection.autocommit = True

    def create_tables(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    id SERIAL PRIMARY KEY,
                    company_id VARCHAR(50) UNIQUE NOT NULL,
                    name VARCHAR(255),
                    url VARCHAR(255),
                    description TEXT,
                    industry VARCHAR(255),
                    size VARCHAR(50),
                    website VARCHAR(255)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    vacancy_id VARCHAR(50) UNIQUE NOT NULL,
                    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
                    name VARCHAR(255),
                    description TEXT,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    salary_currency VARCHAR(10),
                    url VARCHAR(255),
                    published_at TIMESTAMP
                );
            """)

    def insert_company(self, company_data):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO companies (company_id, name, url, description, industry, size, website)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (company_id) DO NOTHING;
            """, (
                company_data.get('id'),
                company_data.get('name'),
                company_data.get('url'),
                company_data.get('description'),
                company_data.get('industry'),
                company_data.get('size'),
                company_data.get('site_url')
            ))

    def insert_vacancy(self, vacancy_data, company_db_id):
        with self.connection.cursor() as cursor:
            salary_from = vacancy_data['salary']['from'] if vacancy_data['salary'] else None
            salary_to = vacancy_data['salary']['to'] if vacancy_data['salary'] else None
            salary_currency = vacancy_data['salary']['currency'] if vacancy_data['salary'] else None

            cursor.execute("""
                INSERT INTO vacancies (vacancy_id, company_id, name, description, salary_from, salary_to, salary_currency, url, published_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, to_timestamp(%s))
                ON CONFLICT (vacancy_id) DO NOTHING;
            """, (
                vacancy_data.get('id'),
                company_db_id,
                vacancy_data.get('name'),
                vacancy_data.get('description'),
                salary_from,
                salary_to,
                salary_currency,
                vacancy_data.get('alternate_url'),
                vacancy_data.get('published_at') / 1000 if vacancy_data.get('published_at') else None
            ))

    def get_companies_and_vacancies_count(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.name, COUNT(v.id) AS vacancies_count
                FROM companies c
                LEFT JOIN vacancies v ON c.id = v.company_id
                GROUP BY c.name;
            """)
            return cursor.fetchall()

    def get_all_vacancies(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.name AS company_name,
                       v.name AS vacancy_name,
                       v.salary_from || '-' || v.salary_to AS salary_range,
                       v.url AS link
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id;
            """)
            return cursor.fetchall()

    def get_avg_salary(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT AVG((salary_from + salary_to)/2.0) FROM vacancies WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
            """)
            result = cursor.fetchone()
            return result[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.name AS company_name,
                       v.name AS vacancy_name,
                       v.salary_from || '-' || v.salary_to AS salary_range,
                       v.url AS link
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                WHERE (v.salary_from + v.salary_to)/2.0 > %s;
            """, (avg_salary,))
            return cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        pattern = f"%{keyword}%"
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.name AS company_name,
                       v.name AS vacancy_name,
                       v.salary_from || '-' || v.salary_to AS salary_range,
                       v.url AS link
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                WHERE LOWER(v.name) LIKE LOWER(%s);
            """, (pattern,))
            return cursor.fetchall()
