#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import sys
import unittest
from unittest.mock import patch


sys.path.append("../src")
from idz import DirectoryViewer, parse_arguments


class TestDirectoryViewer(unittest.TestCase):
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.test_dir = pathlib.Path("test_dir")
        self.test_dir.mkdir(exist_ok=True)

        # Создаем тестовые файлы и каталоги.
        (self.test_dir / "file1.txt").touch()
        (self.test_dir / "file2.txt").touch()
        (self.test_dir / ".hidden_file").touch()
        (self.test_dir / "subdir").mkdir(exist_ok=True)

    def tearDown(self):
        """Очистка после каждого теста."""
        for item in self.test_dir.iterdir():
            if item.is_dir():
                for subitem in item.iterdir():
                    subitem.unlink()
                item.rmdir()
            else:
                item.unlink()
        self.test_dir.rmdir()

    def test_tree_all_files(self):
        """Тест: отображение всех файлов, включая скрытые."""
        args = parse_arguments(["test_dir", "-a"])
        viewer = DirectoryViewer(args)

        with patch("builtins.print") as mock_print:
            viewer.tree(self.test_dir)
            mock_print.assert_any_call("├── file1.txt")
            mock_print.assert_any_call("├── file2.txt")
            mock_print.assert_any_call("├── .hidden_file")
            mock_print.assert_any_call("└── subdir")

    def test_parse_arguments(self):
        """Тест разбора аргументов командной строки."""
        args = parse_arguments(["test_dir", "-a", "-f"])
        self.assertEqual(args.directory, "test_dir")
        self.assertTrue(args.a)
        self.assertTrue(args.f)
        self.assertFalse(args.d)
        self.assertIsNone(args.p)


if __name__ == "__main__":
    unittest.main()
