#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Для примера 1 лабораторной работы 14 добавьте аннотации типов.

import logging
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import date
from typing import List


# Класс пользовательского исключения в случае, если неверно введен номер года.
class IllegalYearError(Exception):
    def __init__(self, year, message="Illegal year number"):
        self.year = year
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.year} -> {self.message}"


# Класс пользовательского исключения в случае, если введенная команда является недопустимой.
class UnknownCommandError(Exception):
    def __init__(self, command, message="Unknown command"):
        self.command = command
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.command} -> {self.message}"


@dataclass(frozen=True)
class Worker:
    name: str
    post: str
    year: int


@dataclass
class Staff:
    workers: List[Worker] = field(default_factory=lambda: [])

    def add(self, name: str, post: str, year: int) -> None:
        # Получить текущую дату.
        today = date.today()

        if year < 0 or year > today.year:
            raise IllegalYearError(year)
        self.workers.append(Worker(name=name, post=post, year=year))

        self.workers.sort(key=lambda worker: worker.name)

    def __str__(self) -> str:
        # Заголовок таблицы.
        table = []
        line = "+-{}-+-{}-+-{}-+-{}-+".format("-" * 4, "-" * 30, "-" * 20, "-" * 8)
        table.append(line)
        table.append("| {:^4} | {:^30} | {:^20} | {:^8} |".format("№", "Ф.И.О.", "Должность", "Год"))
        table.append(line)

        # Вывести данные о всех сотрудниках.
        for idx, worker in enumerate(self.workers, 1):
            table.append("| {:>4} | {:<30} | {:<20} | {:>8} |".format(idx, worker.name, worker.post, worker.year))

        table.append(line)
        return "\n".join(table)

    def select(self, period: int) -> List[Worker]:
        # Получить текущую дату.
        today = date.today()

        result: List[Worker] = []
        for worker in self.workers:
            if today.year - worker.year >= period:
                result.append(worker)

        return result

    def load(self, filename: str) -> None:
        with open(filename, "r", encoding="utf8") as fin:
            xml = fin.read()

        parser = ET.XMLParser(encoding="utf8")
        tree = ET.fromstring(xml, parser=parser)

        self.workers = []
        for worker_element in tree:
            name, post, year = None, None, None

            for element in worker_element:
                if element.tag == "name":
                    name = element.text
                elif element.tag == "post":
                    post = element.text
                elif element.tag == "year":
                    year = int(element.text)

                if name is not None and post is not None and year is not None:
                    self.workers.append(Worker(name=name, post=post, year=year))

    def save(self, filename: str) -> None:
        root = ET.Element("workers")
        for worker in self.workers:
            worker_element = ET.Element("worker")

            name_element = ET.SubElement(worker_element, "name")
            name_element.text = worker.name

            post_element = ET.SubElement(worker_element, "post")
            post_element.text = worker.post

            year_element = ET.SubElement(worker_element, "year")
            year_element.text = str(worker.year)

            root.append(worker_element)

        tree = ET.ElementTree(root)
        with open(filename, "wb") as fout:
            tree.write(fout, encoding="utf8", xml_declaration=True)


if __name__ == "__main__":
    # Выполнить настройку логгера.
    logging.basicConfig(filename="workers4.log", level=logging.INFO)

    # Список работников.
    staff = Staff()

    # Организовать бесконечный цикл запроса команд.
    while True:
        try:
            # Запросить команду из терминала.
            command = input(">>> ").lower()

            # Выполнить действие в соответствие с командой.
            if command == "exit":
                break

            elif command == "add":
                # Запросить данные о работнике.
                name = input("Фамилия и инициалы? ")
                post = input("Должность? ")
                year = int(input("Год поступления? "))

                # Добавить работника.
                staff.add(name, post, year)
                logging.info(f"Добавлен сотрудник: {name}, {post}, " f"поступивший в {year} году.")

            elif command == "list":
                # Вывести список.
                print(staff)
                logging.info("Отображен список сотрудников.")

            elif command.startswith("select "):
                # Разбить команду на части для выделения номера года.
                parts = command.split(maxsplit=1)
                period = int(parts[1])
                selected = staff.select(period)

                # Вывести результаты запроса.
                if selected:
                    for idx, worker in enumerate(selected, 1):
                        print(f"{idx:>4}: {worker.name}")
                else:
                    print("Работники с заданным стажем не найдены.")
                logging.info(f"Найдено {len(selected)} работников со стажем более {period} лет.")

            elif command.startswith("load "):
                # Разбить команду на части для имени файла.
                parts = command.split(maxsplit=1)
                # Загрузить данные из файла.
                staff.load(parts[1])
                logging.info(f"Загружены данные из файла {parts[1]}.")

            elif command.startswith("save "):
                # Разбить команду на части для имени файла.
                parts = command.split(maxsplit=1)
                # Сохранить данные в файл.
                staff.save(parts[1])
                logging.info(f"Сохранены данные в файл {parts[1]}.")

            elif command == "help":
                # Вывести справку о работе с программой.
                print("Список команд:\n")
                print("add - добавить работника;")
                print("list - вывести список работников;")
                print("select <стаж> - запросить работников со стажем;")
                print("load <имя_файла> - загрузить данные из файла;")
                print("save <имя_файла> - сохранить данные в файл;")
                print("help - отобразить справку;")
                print("exit - завершить работу с программой.")

            else:
                raise UnknownCommandError(command)

        except Exception as exc:
            logging.error(f"Ошибка: {exc}")
            print(exc, file=sys.stderr)
