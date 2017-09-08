from pandas import *
import csv, itertools, json, os
import tempfile

import pandas as pd

'''
This utility converts the training data into a format that can be displayed easily with d3 and java.
it converts a flat CSV file to a hierarchical json. It should be able to handle a csv with different column lengths,
but as I don't need this I haven't tested it.

Author: Eli Goldberg December, 2015; updated September 2017; Special thanks to Sami Galal.

'''

# python2 or python3 check
try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str, bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring


class Csv2Flare2:
    def __init__(self, training_headers, training_path, output_path):
        assert all(isinstance(training_header, basestring) for training_header in training_headers)
        self.training_headers = training_headers
        assert isinstance(training_path, basestring)
        self.training_path = training_path
        assert isinstance(output_path, basestring)
        self.output_path = output_path

    def xstr(self, s):
        if s is None:
            return ''
        else:
            return str(s)

    def __json_cluster(self, processed_rows):
        """
        outputs csv data in flare format
        :param processed_rows: row input in csv format
        :return: json as a string
        """
        result = []

        def first_element(x):
            return x[0] if x and isinstance(x, list) else None

        for key, item in itertools.groupby(processed_rows, first_element):
            group_rows = [row for row in item]
            last_row = group_rows[-1]
            group_rows = [row[1:] for row in group_rows]

            if last_row is not None and len(last_row[1:]) == 1:
                try:
                    result.append({"name": last_row[0], "size": float(last_row[1])})
                except:
                    result.append({"name": last_row[0], "size": str(last_row[1])})
            else:
                result.append({"name": key, "children": self.__json_cluster(group_rows)})

        return result

    def __generate_json_file_output(self, processed_rows, output_path):
        """
        wraps the output of the json flare document in some nice text and writes it to file
        :param processed_rows: row input in csv format
        :param output_path: output location for json file
        :return:
        """
        temp = tempfile.NamedTemporaryFile(mode='wt', delete=False)
        temp.write('{"name": "flare",\n')
        temp.write('"children": ')
        json.dump(self.__json_cluster(processed_rows), temp, ensure_ascii=False, indent=2)
        temp.write('\n}\n\n')
        temp.flush()
        temp.close()

        with open(output_path, 'wt') as out_file:
            with open(temp.name, 'rt') as json_file:
                out_rows = json_file.readlines()
                out_file.writelines(out_rows)
        os.unlink(temp.name)

    def __generate_csv_list_output(self, training_data_pd, training_headers):
        """
        reads in some training data in csv and returns it as a list
        :param training_data_pd: pandas dataframe containing training data
        :param training_headers: a list of headers to extract from the dataframe
        :return: csv as string
        """
        training_data_pd.sort_values(training_headers, inplace=True)
        temp = tempfile.NamedTemporaryFile(mode='wt', delete=False)
        # Write to temp file as csv...
        training_data_pd.to_csv(temp.name, na_rep='-', header=False, index=False, encoding='utf-8')
        # ...and read out using csv module
        with open(temp.name, 'rt') as csv_file:
            csv_reader = csv.reader(csv_file)
            csv_list = list(csv_reader)
        os.unlink(temp.name)
        return csv_list

    def convert(self):
        """
        generates json file with flare data from a csv file
        :return:
        """
        training_data_pd = pd.read_csv(self.training_path)
        training_data_pd = training_data_pd[self.training_headers]
        print(training_data_pd.head())

        processed_rows = self.__generate_csv_list_output(training_data_pd, self.training_headers)

        self.__generate_json_file_output(processed_rows, self.output_path)


def main(training_headers):
    # Set the name for input and output files
    # "/Users/future/PycharmProjects/javaJunk/basic_table.csv"
    file_name_pattern = 'matskep'
    training_path = os.path.join(file_name_pattern + '.csv')
    output_path = os.path.join(file_name_pattern + '_flare.json')

    c2f = Csv2Flare2(training_headers, training_path, output_path)
    c2f.convert()


if __name__ == "__main__":
    # Define the grouping order for your dataset
    grouping_order = ['Method',
                      'Methods to Capture Endpoints',
                      'Therapeutic Area',
                      'Target',
                      'Comorbidities',
                      'Known Affects',
                      'Reference',
                      'Data',
                      'Functionality',
                      ]

    main(grouping_order)
