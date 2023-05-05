import csv

def read_csv(file_path):
    keys = []
    athletes_list = []
    header = True
    with open(file_path, 'r',encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, )
        for row in csvreader:
            if header:
                keys = format_headers(row)
                header = False
            else:
                athlete = {}
                for column in range(len(row) - 1):
                    athlete[keys[column]] =  row[column]
                athletes_list.append(athlete)
    return athletes_list


def format_headers(headers):
    formatted = []
    for header in headers:
        if header not in formatted:
            formatted.append(header)
        else:
            i = 1
            name = f'{header}.{i}'
            while f'{header}.{i}' in formatted:
                i += 1
                name = f'{header}.{i}'
            formatted.append(name)
    return formatted