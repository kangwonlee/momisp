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
        self.without_button_filename = "test_add_colab_main_buttons_without_button.ipynb"
        self.without_button_folder = os.path.abspath(os.path.dirname(__file__))
        self.without_button_full_path = os.path.join(self.without_button_folder, self.without_button_filename)

        self.with_button_filename = "test_add_colab_main_buttons_with_button.ipynb"
        self.with_button_folder = os.path.abspath(os.path.dirname(__file__))
        self.with_button_full_path = os.path.join(self.with_button_folder, self.with_button_filename)

        return super().setUp()

    def test_temp_files_have_cells(self):
        nb_without = nbformat.read(self.without_button_full_path, nbformat.NO_CONVERT)
        assert "cells" in nb_without

        nb_with = nbformat.read(self.with_button_full_path, nbformat.NO_CONVERT)
        assert "cells" in nb_with


if "__main__" == __name__:
    unittest.main()
