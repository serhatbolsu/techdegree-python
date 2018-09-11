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

    def find_by_keyword(self,keyword):
        with open(self.file) as f:
            data = f.read()
            regex = re.compile(r'\d{2}\/\d{2}\/\d{4},%s,[\d]+,[\w ]+' % keyword)
            result = re.findall(regex, data)

            re_string = r'.*(?={}).*'.format(keyword)
            regex = re.compile(re_string)
            result2 = re.findall(regex, data)
        final_result = result + result2
        return set(final_result)

    def find_by_time_spent(self, time_spend):
        with open(self.file) as f:
            data = f.read()
            regex = re.compile(r'[\d/]+,[\w\d]+,%s,[\w ]+' % str(time_spend))
            result = re.findall(regex, data)
        return result

    #TODO: Fix the result pattern
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
    mycsv = CsvOperation('work_log.csv')
    # mycsv.output_to_csv(date= "25/08/1984", "my name", "24 hours")
    print(mycsv.find_by_date("10/09/2018"))
    print(mycsv.find_by_keyword("unit1"))
    print(mycsv.find_by_time_spent(30))
    print(mycsv.find_by_regex_pattern("([^\s].*)"))
    print(mycsv.delete_row("10/09/2018,unit6,46,almost finished and I am gbloobb"))



