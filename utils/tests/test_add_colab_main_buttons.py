import os
import sys
import unittest


import nbformat


sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), os.pardir
        )
    )
)


import add_colab_main_buttons as acb


class TestAddColabMainButtons(unittest.TestCase):
    def setUp(self) -> None:
        self.no_button_filename = "test_add_colab_main_buttons_without_button.ipynb"
        self.no_button_folder = os.path.abspath(os.path.dirname(__file__))
        self.no_button_full_path = os.path.join(self.no_button_folder, self.no_button_filename)

        return super().setUp()

    def test_temp_file(self):
        nb = nbformat.read(self.no_button_full_path, nbformat.NO_CONVERT)
        assert "cells" in nb


if "__main__" == __name__:
    unittest.main()
