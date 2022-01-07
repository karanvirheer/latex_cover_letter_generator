from PyPDF2 import PdfFileMerger
import pandas as pd
import argparse
import os
import subprocess
from pathlib import Path
from string import Template
import datetime


class MyTemplate(Template):
    delimiter = '>'


class Generator:

    def __init__(self, config_info: dict) -> None:
        self.config_info = config_info
        self.variable_dict = config_info["VARIABLE_DICT"]
        self.template_dir = config_info["TEMPLATE_DIR"]
        self.save_dir = config_info["SAVE_DIR"]
