import openpyxl
import glob2

# Pobierz listę wszystkich plików xlsx w bieżącym katalogu
xlsx_files = glob2.glob('*.xlsx')
print(xlsx_files)

# Dla każdego pliku xlsx
for xlsx_file in xlsx_files:
    # Otwórz plik Excel
    wb = openpyxl.load_workbook(xlsx_file)
    print(wb)

    # Pobierz wszystkie arkusze
    sheets = wb.sheetnames
    print(sheets)

    # Dla każdego arkusza
    for sheet in sheets:
        # Pobierz arkusz
        ws = wb[sheet]
        # Dla każdego wiersza i każdej kolumny
        for row in ws.rows:
            for cell in row:
                # Jeśli wartość komórki to "Tomasz Testowy"
                if cell.value == "Janusz Piwko":
                    # Zamień wartość komórki na "Tester Realestate"
                    cell.value = "Tester CRM"

    # Zapisz plik Excel
    wb.save(xlsx_file)