# SENCHAADDATTR
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from urllib.parse import unquote
import xlsxwriter
from flask import render_template
import os
import io
import time
import openpyxl
from flask import send_file

app = Flask(__name__)

class Phraser():
    def __init__(self):
        self.HTMLFile = None
        self.index = None
        self.S = None
        self.list_values = []
        self.tag_name = None
        self.outWorkbook = None
        self.outSheet = None
        self.value = None

    def parse_html(self, html, parse_type):
        if parse_type == "senchatest":
            self.parse_senchatest(html)
        elif parse_type == "fieldText":
            self.parse_fieldText(html)
    
    def parse_senchatest(self, html): # funkcja do wyciagania obiektów senchatest
        self.HTMLFile = html
        self.S = BeautifulSoup(self.HTMLFile, 'lxml')
        self.tag_name = self.S.find_all('div')

        for self.tag in self.tag_name:
            if 'senchatest=' in str(self.tag):
                self.tag = str(self.tag)
                self.sencha = self.tag.partition("senchatest=")[2]
                self.sencha = self.sencha.split("\"")[1]
                if 'type="text"' in str(self.tag):
                    self.typ_pola = 'string'
                elif self.tag.find('button') != -1:
                    self.typ_pola = 'click'
                else:
                    self.typ_pola = ''
                self.list_values.append((self.sencha, self.typ_pola))  # Change this line

    def parse_fieldText(self, html): # funkcja do wyciągania obiektów z atrybutów - fieldów nie położonych
        self.HTMLFile = html
        self.S = BeautifulSoup(self.HTMLFile, 'lxml')
        self.tag_name = self.S.find_all('span', {'style': 'color:#999999'})

        for self.tag in self.tag_name:
            self.text = self.tag.get_text()
            self.parent_div = self.tag.parent
            self.second_text = None

            for node in self.parent_div.contents:
                if isinstance(node, str) and node.strip() and node[0].isupper():
                    self.second_text = node.strip()
                    break

            self.list_values.append((self.text, 'DragAndDrop', self.second_text))

    def generate_excel(self):
        output_dir = "C:\\Users\\root2\\Katalon\\Katalon dataFiles\\Generated-Excel-Files"
        timestamp = int(time.time())
        output_filename = f"praca_{timestamp}.xlsx"
        output_path = os.path.join(output_dir, output_filename)

        self.outWorkbook = xlsxwriter.Workbook(output_path)
        self.outSheet = self.outWorkbook.add_worksheet()
        self.value = list(self.list_values)
        self.outSheet.write("A1", "fieldName")
        self.outSheet.write("B1", "fieldType")
        self.outSheet.write("C1", "fieldText")

        for item in range(len(self.value)):
            self.outSheet.write(item+1, 0, self.value[item][0])
            self.outSheet.write(item+1, 1, self.value[item][1])

            if len(self.value[item]) > 2:
                self.outSheet.write(item+1, 2, self.value[item][2])

        self.outWorkbook.close()

        return self.list_values

#ZAMIENIATOR REPLACER DEKODUJĄCY
def replace_characters(input_string):
    decoded_string = unquote(input_string)
    temp = decoded_string.replace("=", ":")
    result = temp.replace("&", "\n")
    return result

@app.route('/replacer', methods=['GET', 'POST'])
def replacer():
    if request.method == 'POST':
        text = request.form['text']
        result = replace_characters(text)
        return render_template('form3.html', result=result)
    return render_template('form3.html')

@app.route('/generate_excel', methods=['POST'])
def generate_excel_route():
    phraser = Phraser()
    parse_type = request.form['parse_type']
    phraser.parse_html(request.form['html'], parse_type)
    phraser.generate_excel()

    found_objects = phraser.generate_excel()  # Get list of found objects

    # zwraca wygenerowany plik Excel jako JSON
    return jsonify({'result': 'success', 'message': 'Plik .xlsx został wygenerowany!', 'found_objects': found_objects})


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # generuj plik Excel na podstawie kodu HTML z formularza
        generate_excel_route()
    # renderuj stronę HTML z formularzem do wprowadzenia kodu HTML
    return render_template('form2.html')

if __name__ == '__main__':
    app.run(debug=True)