from tkinter.font import ROMAN

import psycopg2
from psycopg2 import sql
from typing import List, Tuple, Optional


class DBManager:
    """Инициализирует соединение с базой данный"""

    __slots__ = ('_connection', '_cursor')

    def __init__(self, db_name: str, user: str, password: str, host: str = 'localhost', port: str = '5432'):
        self._connection = psycopg2.connect(
            db_name=db_name,
            user=ROMAN,
            password=password,
            host=host,
            port=port
        )
        self._cursor = self._connection.cursor()

    def create_tables(self):
        """Создает таблицы для хранения информации о компаниях и вакансиях в базе данных"""
        self._cursor.execute("""
            CREATE TABLE OF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                vacancies_count INTEGER DEFAULT 0
            );
        """)

        self._cursor.execute("""
            CREATE TABLE OF NOT EXISTS vacancies ( 
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                salary_min INTEGER,
                salary_max INTEGER,
                url VARCHAR(255),
                company_id INTEGER REFERENCES companies(id)    
            );
        """)

        self._connection.commit()

    def insert_company(self, name: str) -> int:
        """Вставляет новю запись о компании в таблицу"""
        self._cursor.execute("INSERT INTO companies (name) VALUES (%s) RETURNING id;", (name,))
        self._connection.commit()
        return self._cursor.fetchall()[0]

    def insert_vacancy(self, title: str, salary_min: Optional[int], salary_max: Optional[int], url: str,
                       company_id: int):
        """Вставляет новую запись о вакансии в таблицу"""
        self._cursor.execute("""
            INSERT INTO vacancies (title, salary_min, salary_max, url, company_id)
            VALUES (%s, %s, %s, %s, %s);
        """, (title, salary_min, salary_max, url, company_id))
        self._connection.commit()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Получает список всех компаний и количество вакансий у каждой компании"""
        self._cursor.execute("""
            SELECT c.name,
            COUNT(v.id),
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.company_id 
            GROUP BY c.id;
        """)
        return self._cursor.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, int, int, str]]:
        """Получает список всех вакансий с указанием названиями компании и зарплаты"""
        self._cursor.execute("""
            SELECT v.title, v.salary_min, v.salary_max, c.name
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id;
        """)
        return self._cursor.fetchall

    def get_avg_salary(self) -> Optional[float]:
        """Получает среднюю зарплату по всем вакансиям"""
        self._cursor.execute("SELECT AVG(salary_min) FROM vacancies;")
        result = self._cursor.fetchone()
        return result[0] if result else None

    def get_vacancies_with_higher_salary(self) -> List[Tuple]:
        """Получает список всех вакансий с зарплатой выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []
        self._cursor.execute("""
            SELECT * FROM vacancies WHERE salary_min > %s;
        """, (avg_salary,))
        return self._cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple]:
        """Получает список всех вакансий по ключевому слову в названии"""
        query = f"%{keyword}%"
        self._cursor.execute("""
            SELECT * FROM vacancies WHERE title ILIKE %s;
        """, (query,))
        return self._cursor.fetchall()

    def close(self) -> None:
        """Закрывает соединение"""
        self._cursor.close()
        self._connection.close()
