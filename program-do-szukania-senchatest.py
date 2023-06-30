from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import xlsxwriter
from flask import render_template
import os
import time

app = Flask(__name__)

class Phraser():
    def __init__(self):
        self.HTMLFile = None
        self.index = None
        self.S = None
        self.list_values = []  # Change this line
        self.tag_name = None
        self.outWorkbook = None
        self.outSheet = None
        self.value = None

    def parse_html(self, html):
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

    def generate_excel(self):
        output_dir = "C:\\Users\\root2\\Katalon\\Katalon dataFiles\\Generated-Excel-Files"
        timestamp = int(time.time())
        output_filename = f"praca_{timestamp}.xlsx"
        output_path = os.path.join(output_dir, output_filename)

        self.outWorkbook = xlsxwriter.Workbook(output_path)
        self.outSheet = self.outWorkbook.add_worksheet()
        self.value = list(self.list_values)
        self.outSheet.write("A1", "senchatest")
        self.outSheet.write("B1", "typPola")
        self.outSheet.write("C1", "trescPola")
        self.outSheet.write("D1", "weryfikacja")

        for item in range(len(self.value)):
            self.outSheet.write(item+1, 0, self.value[item][0])
            self.outSheet.write(item+1, 1, self.value[item][1])

        self.outWorkbook.close()

@app.route('/generate_excel', methods=['POST'])
def generate_excel():
    phraser = Phraser()
    phraser.parse_html(request.form['html'])
    phraser.generate_excel()

    # zwraca wygenerowany plik Excel jako JSON
    return jsonify({'result': 'success', 'message': 'Plik .xlsx został wygenerowany!'})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # generuj plik Excel na podstawie kodu HTML z formularza
        generate_excel()
    # renderuj stronę HTML z formularzem do wprowadzenia kodu HTML
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
