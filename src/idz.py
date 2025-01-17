#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# выполнить индивидуальное задание 2 лабораторной работы 2.19, добавив аннтотации типов. Выполнить проверку программы
# с помощью утилиты mypy.

import argparse
import pathlib
import subprocess
from typing import List, Optional, Protocol


class TypeChecker(Protocol):
    """Протокол для проверки типов в файле."""

    def check_types(self) -> None:
        """Запускает проверку типов."""
        pass


class MypyTypeChecker:
    """Класс для проверки аннотаций типов с использованием mypy."""

    def check_types(self) -> None:
        try:
            result = subprocess.run(["mypy", __file__], capture_output=True, text=True)
            if result.returncode == 0:
                print("Проверка типов с mypy завершена успешно. Ошибок не найдено.")
            else:
                print("Ошибки проверки типов с mypy:")
                print(result.stdout)
        except FileNotFoundError:
            print("mypy не установлен. Установите его с помощью 'pip install mypy'.")


class DirectoryViewer:
    """Класс для отображения содержимого каталога с учетом фильтров."""

    def __init__(self, args: argparse.Namespace):
        self.args = args

    def tree(self, directory: pathlib.Path, prefix: str = "", level: int = 0) -> None:
        """Рекурсивный вывод содержимого каталога с учетом аргументов командной строки."""
        # Проверка на None и преобразование
        if self.args.p is not None and level > int(self.args.p):  # Добавляем проверку на None
            return

        contents = self.get_directory_contents(directory)
        decoration = ["├── "] * (len(contents) - 1) + ["└── "]

        for pointer, path in zip(decoration, contents):
            display_path = str(path) if self.args.t else path.name
            print(prefix + pointer + display_path)

            if path.is_dir():
                new_prefix = prefix + ("│   " if pointer == "├── " else "    ")
                self.tree(path, prefix=new_prefix, level=level + 1)

    def get_directory_contents(self, directory: pathlib.Path) -> List[pathlib.Path]:
        """Возвращает отфильтрованное содержимое каталога в зависимости от аргументов командной строки."""
        contents = list(directory.iterdir())

        if not self.args.a:
            contents = [file for file in contents if not file.name.startswith(".")]

        if self.args.d:
            contents = [file for file in contents if file.is_dir()]

        if self.args.f:
            contents = [file for file in contents if file.is_file()]

        return contents


def parse_arguments(command_line: Optional[List[str]] = None) -> argparse.Namespace:
    """Разбирает аргументы командной строки и возвращает объект Namespace."""
    parser = argparse.ArgumentParser(description="Аналог команды tree в Linux.")
    parser.add_argument("directory", type=str, help="The directory to list.")
    parser.add_argument("-a", action="store_true", help="List all files, including hidden files.")

    choose = parser.add_mutually_exclusive_group()
    choose.add_argument("-d", action="store_true", help="List directories only.")
    choose.add_argument("-f", action="store_true", help="List files only.")

    parser.add_argument("-p", type=int, help="Max display depth of the directory tree.")
    parser.add_argument("-t", action="store_true", help="Print the full path prefix for each file.")
    parser.add_argument("--version", action="version", version="%(prog)s 0.0.1")

    return parser.parse_args(command_line)


def main(command_line: Optional[List[str]] = None, type_checker: Optional[TypeChecker] = None) -> None:
    """Основная функция программы."""
    # Проверка типов, если предоставлен TypeChecker.
    if type_checker:
        type_checker.check_types()

    args = parse_arguments(command_line)
    directory = pathlib.Path(args.directory).resolve(strict=True)

    # Создаем объект для отображения дерева и выводим содержимое каталога.
    viewer = DirectoryViewer(args)
    viewer.tree(directory)


if __name__ == "__main__":
    # Основная функция вызывается с проверкой типов через MypyTypeChecker.
    main(type_checker=MypyTypeChecker())
