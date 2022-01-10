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
        self.variable_dict = config_info["VAR_TO_INPUT_DIC"]

        template_dir = os.path.split(config_info["TEMPLATE_DIR"])
        self.template_dir = Path(
            template_dir[0] + '\\' + template_dir[1]).read_text()

        self.save_dir = config_info["SAVE_DIR"]
        self.tracker_dir = config_info["TRACKER_DIR"]

    def read_excel_sheet(self):
        header_dic = {}
        excel_dataframe = pd.read_excel(self.tracker_dir)
        for header in excel_dataframe.columns:
            if "Unnamed" not in header:
                header_dic[header] = ""
        return header_dic

    def create(self):
        print("\n============ CREATING PDF FILE ============\n")

        with open('cover.tex', 'w') as f:
            s = MyTemplate(self.template_dir)

            f.write(s.substitute(self.variable_dict))

        cmd = ['pdflatex', '-interaction', 'nonstopmode', 'cover.tex']
        proc = subprocess.Popen(cmd)
        proc.communicate()

        print("\n============ DELETING FILES CREATED ============\n")

        os.unlink('cover.tex')
        os.unlink('cover.log')
        os.unlink('cover.aux')
        os.unlink('cover.out')
