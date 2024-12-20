#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from datetime import date
import sys

sys.path.append('../src')
from src.primer import Staff, IllegalYearError, UnknownCommandError


class TestStaff(unittest.TestCase):
    def setUp(self):
        """Создаем объект Staff перед каждым тестом"""
        self.staff = Staff()

    def test_add_worker(self):
        """Тест добавления нового сотрудника"""
        self.staff.add(name="Иванов И.И.", post="Инженер", year=2015)
        self.assertEqual(len(self.staff.workers), 1)
        self.assertEqual(self.staff.workers[0].name, "Иванов И.И.")
        self.assertEqual(self.staff.workers[0].post, "Инженер")
        self.assertEqual(self.staff.workers[0].year, 2015)

    def test_add_worker_invalid_year(self):
        """Тест добавления сотрудника с некорректным годом"""
        with self.assertRaises(IllegalYearError):
            self.staff.add(name="Иванов И.И.", post="Инженер", year=3000)

    def test_select_worker_by_period(self):
        """Тест выбора сотрудников по стажу"""
        current_year = date.today().year
        self.staff.add(name="Иванов И.И.", post="Инженер", year=current_year - 10)
        self.staff.add(name="Петров П.П.", post="Менеджер", year=current_year - 3)

        selected = self.staff.select(5)
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].name, "Иванов И.И.")

    def test_save_and_load(self):
        """Тест сохранения и загрузки сотрудников из XML"""
        self.staff.add(name="Иванов И.И.", post="Инженер", year=2015)
        self.staff.add(name="Петров П.П.", post="Менеджер", year=2010)

        # Сохранение данных
        filename = "../src/test_workers.xml"
        self.staff.save(filename)

        # Создаем новый объект Staff и загружаем данные
        new_staff = Staff()
        new_staff.load(filename)

        self.assertEqual(len(new_staff.workers), 2)
        self.assertEqual(new_staff.workers[0].name, "Иванов И.И.")
        self.assertEqual(new_staff.workers[1].name, "Петров П.П.")

    def test_unknown_command_error(self):
        """Тест пользовательского исключения UnknownCommandError"""
        with self.assertRaises(UnknownCommandError) as context:
            raise UnknownCommandError(command="unknown")
        self.assertEqual(str(context.exception), "unknown -> Unknown command")


if __name__ == "__main__":
    unittest.main()