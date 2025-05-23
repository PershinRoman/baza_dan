import psycopg2


class DBManager:
    def __init__(self, config):
        """
        Инициализация подключения к базе данных.
        config — словарь с параметрами подключения:
            {
                'host': 'localhost',
                'database': 'your_db_name',
                'user': 'your_username',
                'password': 'your_password'
            }
        """
        self.connection = psycopg2.connect(**config)
        self.cursor = self.connection.cursor()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        Возвращает список кортежей: [(company_name, vacancies_count), ...]
        """
        query = """
            SELECT c.name, COUNT(v.id) AS vacancies_count
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.id, c.name;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        query = """
            SELECT c.name, v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        query = """
            SELECT AVG((salary_from + salary_to)/2) FROM vacancies WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        # Предположим, что вы ищете вакансии с зарплатой выше средней
        avg_salary = self.get_avg_salary()
        query = """
            SELECT c.name, v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE v.salary_from > %s OR v.salary_to > %s;
        """
        self.cursor.execute(query, (avg_salary, avg_salary))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        search_pattern = f"%{keyword}%"
        query = """
            SELECT c.name, v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE v.name ILIKE %s OR v.description ILIKE %s;
        """
        self.cursor.execute(query, (search_pattern, search_pattern))
        return self.cursor.fetchall()


def close(self):
    # закрытие курсора и соединения
    if self.cursor:
        self.cursor.close()
    if self.connection:
        self.connection.close()


config = {
    'host': 'localhost',
    'database': 'baza_dan',
    'user': 'postgres',
    'password': '159'
}

db_manager = DBManager(config)

# Получить компании и количество вакансий
companies_vacancies = db_manager.get_companies_and_vacancies_count()
print(companies_vacancies)

# Получить все вакансии
all_vacancies = db_manager.get_all_vacancies()
print(all_vacancies)

# Средняя зарплата
avg_salary = db_manager.get_avg_salary()
print(avg_salary)

# Вакансии с зарплатой выше средней
higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
print(higher_salary_vacancies)

# Вакансии по ключевому слову "Python"
python_vacancies = db_manager.get_vacancies_with_keyword("Python")
print(python_vacancies)
