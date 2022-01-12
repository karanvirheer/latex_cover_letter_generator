from PyPDF2 import PdfFileMerger
import pandas as pd
import argparse
import os
import subprocess
from pathlib import Path
from string import Template
import random


class MyTemplate(Template):
    delimiter = '>'


class Generator:

    def __init__(self, config_info: dict) -> None:
        self.config_info = config_info

        if os.path.exists("settings.pickle"):
            self.variable_dict = config_info.get("VAR_TO_INPUT_DIC", {})

            template_dir = os.path.split(config_info["TEMPLATE_DIR"])
            self.template_dir = Path(
                template_dir[0] + '\\' + template_dir[1]).read_text()

            self.save_dir = config_info["SAVE_DIR"]
            self.tracker_dir = config_info["TRACKER_DIR"]

            self.excel_dataframe = pd.read_excel(self.tracker_dir)

    def read_excel_sheet(self):
        header_dic = {}
        for header in self.excel_dataframe.columns:
            if "Unnamed" not in header:
                header_dic[header] = ""
        return header_dic

    def write_to_excel_sheet(self):
        self.excel_dataframe = self.excel_dataframe.append(
            self.config_info["HEADER_TO_INPUT_DIC"], ignore_index=True)

        self.excel_dataframe.to_excel(self.tracker_dir, index=False)

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

    def save_pdf(self):
        output_path = f"{self.config_info['SAVE_DIR']}//{self.config_info['FILE_NAME']}.pdf"
        if (os.path.exists(output_path)):
            num = random.randint(0, 1000)
            output_path = f"{self.config_info['SAVE_DIR']}//{self.config_info['FILE_NAME']} ({num}).pdf"

        input_path = os.path.abspath('cover.pdf')
        cmd = ['copy', input_path, output_path]
        subprocess.call(cmd, shell=True)
