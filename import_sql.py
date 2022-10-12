import sqlite3
import csv
import json
import xml.etree.ElementTree as ET

class Import:
    def import_file(self, filename):
        if filename[-4:] == '.csv':
            self.import_csv(filename)
        elif filename[-5:] == '.json':
            self.import_json(filename)
        elif filename[-4:] == '.xml':
            self.import_xml(filename)

    def import_csv(self, filename):
        table_name = filename[:-4]
        csv_file = csv.DictReader(open(filename, 'r', encoding = 'UTF-8'))
        
        db = sqlite3.connect("data.sqlite")
        cur = db.cursor()
        
        x = []
        x2 = []
        for row in csv_file:
            x = row
            x2 = row.values()
            break
        csv_file = csv.DictReader(open(filename, 'r', encoding = 'UTF-8'))
        str_list = self.table_to_input(x, x2)
        str_list2 = ''
        for col in x:
            str_list2 += col + ', '
        str_list2 = str_list2[:-2]
        cur.execute('DROP TABLE IF EXISTS ' + table_name + ';')
        cur.execute('CREATE TABLE IF NOT EXISTS '+table_name+' (' + str_list + ');')
        for row in csv_file:
            r = row.values()
            list_of_values = ""
            for vals in r:
                if str(vals).isnumeric() == False and self.is_float(str(vals)) == False:
                    list_of_values += '"'+str(vals)+'", '
                else:
                    list_of_values += str(vals) + ", "
            list_of_values = list_of_values[:-2]
            cur.execute('INSERT INTO '+table_name+' ('+str_list2+') VALUES ('+list_of_values+');')
        db.commit()

    def import_json(self, filename):
        table_name = filename[:-5]
        json_file = json.load(open(filename, 'r', encoding='utf-8'))

        db = sqlite3.connect("data.sqlite")
        cur = db.cursor()
        x = []
        x2 = []
        for row in json_file:
            x = row
            x2 = row
            break
        json_file = json.load(open(filename, 'r', encoding='utf-8'))
        str_list = self.table_to_input(x, x2)
        str_list2 = ''
        for col in x:
            str_list2 += col + ', '
        str_list2 = str_list2[:-2]
        cur.execute('DROP TABLE IF EXISTS ' + table_name + ';')
        cur.execute('CREATE TABLE IF NOT EXISTS '+table_name+' (' + str_list + ');')
        for row in json_file:
            r = row.values()
            list_of_values = ""
            for vals in r:
                if str(vals).isnumeric() == False and self.is_float(str(vals)) == False:
                    list_of_values += '"'+str(vals)+'", '
                else:
                    list_of_values += str(vals) + ", "
            list_of_values = list_of_values[:-2]
            cur.execute('INSERT INTO '+table_name+' ('+str_list2+') VALUES ('+list_of_values+');')
        db.commit()

    def import_xml(self, filename):
        table_name = filename[:-4]
        xml_file = ET.parse(filename)
        rt = xml_file.getroot()

        db = sqlite3.connect("data.sqlite")
        cur = db.cursor()

        x = []
        x2 = []
        for row in rt.iter():
            if row.tag in x:
                break
            x.append(row.tag)
            x2.append(row.text)
        x = x[2:]
        x2 = x2[2:]
        xml_file = ET.parse(filename)
        rt = xml_file.getroot()
        str_list = self.table_to_input(x, x2)
        str_list2 = ''
        for col in x:
            str_list2 += col + ', '
        str_list2 = str_list2[:-2]
        cur.execute('DROP TABLE IF EXISTS ' + table_name + ';')
        cur.execute('CREATE TABLE IF NOT EXISTS '+table_name+' (' + str_list + ');')
        for row in rt:
            r = []
            for val in x:
                r.append(row.find(val).text)
            list_of_values = ""
            for vals in r:
                if str(vals).isnumeric() == False and self.is_float(str(vals)) == False:
                    list_of_values += '"'+str(vals)+'", '
                else:
                    list_of_values += str(vals) + ", "
            list_of_values = list_of_values[:-2]
            cur.execute('INSERT INTO '+table_name+' ('+str_list2+') VALUES ('+list_of_values+');')
        db.commit()
    
    def table_to_input(self, x, x2):
        type_list = []
        str_list = ''
        for col in x2:
            if col.isnumeric():
                type_list.append(" INTEGER, ")
            elif self.is_float(col):
                    type_list.append(" REAL, ")
            else:
                type_list.append(" TEXT, ")
        c = 0
        for col in x:
            str_list += col+type_list[c]
            c+=1
        str_list = str_list[:-2]
        return str_list

    def is_float(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
