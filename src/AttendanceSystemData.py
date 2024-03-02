import csv
import os
from collections import defaultdict
from datetime import datetime

from src.PulseDetect import PulseDetect


class Data:
    App = None
    data_path = './data'
    gray_images_path = './data/gray_images/'
    keymap_index = dict()
    keymap_label = dict()
    status_index = defaultdict(bool)

    # records table related
    records_count = 0
    records_table = []      # append not rewrite
    records_table_fields = ['record_id', 'user_id', 'name', 'date', 'check_in', 'check_out']
    records_table_path = './data/records_table.csv'

    # information table related
    info_table = []
    info_table_fields = ['user_id', 'name', 'label']
    info_table_path = './data/info_table.csv'

    @classmethod
    def initialize(cls):
        with open(Data.info_table_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            header = reader.fieldnames
            for row in reader:
                Data.keymap_label[int(row.get('label'))] = (row.get('user_id'), row.get('name'))
                Data.keymap_index[row.get('user_id')] = (row.get('name'), row.get('label'))

        if not os.path.exists(Data.records_table_path):
            file = open(Data.records_table_path, 'w')
        else:
            with open(Data.records_table_path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                last_line = 0
                for line_number, row in enumerate(reader, start=1):
                    last_line = line_number
                Data.records_count = last_line


    @staticmethod
    def fetch_name_by_id(id):
        if id not in Data.keymap_index:
            return None
        else:
            return Data.keymap_index[id][0]

    @staticmethod
    def fetch_name_by_label(label):
        if label >= len(Data.keymap_label):
            return None
        else:
            return Data.keymap_label[label][1]

    @staticmethod
    def fetch_label_by_id(id):
        if id not in Data.keymap_index:
            return None
        else:
            return int(Data.keymap_index[id][1])

    @staticmethod
    def fetch_id_by_label(label):
        if label >= len(Data.keymap_label):
            return None
        else:
            return Data.keymap_label[label][0]

    @staticmethod
    def make_records(label) -> (bool, str, str):
        # return back True or False indicate check-in or out status
        new_record = dict()
        index, name = Data.keymap_label[label]
        right_datetime = datetime.now()
        cur_date = right_datetime.date().strftime('%d/%m/%Y')
        cur_time = right_datetime.time().strftime('%H:%M:%S')
        new_record['user_id'] = index
        new_record['name'] = name
        new_record['record_id'] = Data.records_count
        Data.records_count += 1
        new_record['date'] = cur_date
        new_record['check_in'], new_record['check_out'] = '-', '-'
        if not Data.status_index[index]:
            new_record['check_in'] = cur_time
        else:
            new_record['check_out'] = cur_time
        Data.status_index[index] = not Data.status_index[index]
        Data.records_table.append(new_record)
        return Data.status_index[index], index, name

    @staticmethod
    def update_records_table():
        if not Data.records_table:
            return
        with open(Data.records_table_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=Data.records_table_fields)
            writer.writeheader()
            writer.writerows(Data.records_table)
        Data.records_table = []
    @staticmethod
    def update_info_table():
        # read items in the directory one by one
        label = 0
        for item in os.listdir(Data.gray_images_path):
            id, name = item, None
            dir_path = os.path.join(Data.gray_images_path, item)
            for file in os.listdir(dir_path):
                name = file.split('_')[0]
                break
            Data.info_table.append({
                'user_id': id,
                'name': name,
                'label': label
            })
            label += 1
        # open the csv file and write back
        with open(Data.info_table_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=Data.info_table_fields)
            writer.writeheader()
            writer.writerows(Data.info_table)
        Data.initialize()

    @staticmethod
    def organize_csv_file():
        with open(Data.records_table_path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)

        data_indices = [row for row in data if row[0] != 'record_id']
        chosen_header_index = data[0]
        cleaned_data = [chosen_header_index] + data_indices

        with open(Data.records_table_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(cleaned_data)

    @staticmethod
    def render_data():
        datas = []
        for each in Data.records_table:
            datas.append((
                each.get('user_id'),
                each.get('name'),
                each.get('date'),
                each.get('check_in'),
                each.get('check_out')
            ))
        return datas

    @staticmethod
    def run_detect():
        Data.App = PulseDetect()
        flag = True
        while flag:
            flag = Data.App.main_loop()













