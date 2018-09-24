import csv
import datetime
import re


class CsvOperation:
    def __init__(self, filename='works.csv'):
        self.file = filename
        self.fieldnames = ["date", "name", "time_spend", "notes"]

    def output_to_csv(self, **data):
        row = dict()
        row['date'] = datetime.datetime.now().strftime('%d/%m/%Y')
        row['name'] = data['name']
        row['time_spend'] = data['time_spend']
        row['notes'] = data['notes']
        try:
            with open(self.file, 'a', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writerow(row)
        except:
            with open(self.file, 'w', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerow(row)

    def read_from_csv(self, query):
        pass

    def find_by_date(self, date):
        date = date.strip().split("/")
        with open(self.file) as f:
            data = f.read()
            re_string = '{}/{}/{},[\w ]+,[\d]+,[\w ]+'.format(date[0], date[1], date[2])
            regex = re.compile(re_string)
            result = re.findall(regex, data)
        return result

    def find_by_date_range(self, date1, date2):
        def enumerate_csv_with_dates():
            _result = []
            with open(self.file) as f:
                data = csv.reader(f)
                for i, line in enumerate(data):
                    line = ','.join(line)
                    _d = re.match(r'(\d{2})(\/\d{2})(\/\d{4})', line)[0]
                    date = datetime.datetime.strptime(_d,"%d/%m/%Y")
                    item = {'index': i, 'date': date, 'line': line}
                    _result.append(item)
            return _result
        result = []
        date1 = datetime.datetime.strptime(date1, '%d/%m/%Y')
        date2 = datetime.datetime.strptime(date2, '%d/%m/%Y')
        d_sorted = sorted([date1, date2])
        for item in enumerate_csv_with_dates():
            if d_sorted[0] < item['date'] < d_sorted[1]:
                result.append(item['line'])
        return result

    def find_by_keyword(self,keyword):
        with open(self.file) as f:
            data = f.read()
            # Find in title
            regex = re.compile(r'\d{2}\/\d{2}\/\d{4},%s,[\d]+,[\w ]+' % keyword)
            result = re.findall(regex, data)
            # Find in everywhere, this is an exercise to try regular expressions
            re_string = r'.*(?={}).*'.format(keyword)
            regex = re.compile(re_string)
            result2 = re.findall(regex, data)
        final_result = set(result + result2)
        return list(final_result)

    def find_by_time_spent(self, time_spend):
        result = []
        with open(self.file) as f:
            data = csv.reader(f)
            for line in data:
                if int(line[2]) == int(time_spend):
                    result.append(','.join(line))
        return result

    def find_by_regex_pattern(self, regex):
        re_string = r'{}'.format(regex)
        with open(self.file) as f:
            data = f.read()
            pattern = re.compile(re_string, re.VERBOSE)
            result = re.findall(pattern, data)
        return result

    def delete_row(self, entry):
        inp = open(self.file, newline='')
        data_r = list(csv.reader(inp))

        with open(self.file, 'w', newline='') as out:
            writer = csv.writer(out)
            for row in data_r:
                row_string = ','.join(row)
                if row_string != entry:
                    writer.writerow(row)


if __name__ == '__main__':
    mycsv = CsvOperation('work_log_test.csv')
    # mycsv.output_to_csv(date= "25/08/1984", "my name", "24 hours")
    print("By Date:")
    print(mycsv.find_by_date("10/09/2018"))
    print("By Keyword:")
    print(mycsv.find_by_keyword("unit1"))
    print("By Time:")
    print(mycsv.find_by_time_spent(30))
    print("By Regex:")
    print(mycsv.find_by_regex_pattern("([^\s].*)"))
    print("By Range: ")
    print(mycsv.find_by_date_range("01/10/2018", "30/12/2010"))
    print(mycsv.delete_row("10/09/2018,unit6,46,almost finished and I am gbloobb"))




