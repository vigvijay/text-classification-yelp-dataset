# -*- coding: utf-8 -*-
"""Convert from json format to csv.
"""
import argparse
import collections
import csv
import simplejson as json
from textwrap import TextWrapper


def read_write_file(json_file_path, csv_file_path, columns):
    """Read in the json dataset file and write it out to a csv file, given the column names."""
    with open(csv_file_path, 'w', newline = '') as fout:
        csv_file = csv.writer(fout)
        csv_file.writerow(list(columns))
        with open(json_file_path) as fin:
            for line in fin:
                json_lines = json.loads(line)
                '''w = TextWrapper.wrap(json_lines,width=len(json_lines))'''
                '''json_lines = json_lines.replace_whitespace'''
                '''json_lines = ' '.join(w.wrap(json_lines))'''
                csv_file.writerow(get_row(json_lines, columns))

def get_superset_of_columns_from_file(json_file_path):
    """Read in the json dataset file and return the superset of column names."""
    columns = set()
    with open(json_file_path) as fin:
        for line in fin:
            json_lines = json.loads(line)
            columns.update(
                    set(get_columns(json_lines).keys())
                    )
    return columns

def get_columns(json_lines, parent_key=''):
    
    columns = []
    for k, v in json_lines.items():
        column_name = "{0}.{1}".format(parent_key, k) if parent_key else k
        if isinstance(v, collections.MutableMapping):
            columns.extend(
                    list(get_columns(v, column_name).items())
                    )
        else:
            columns.append((column_name, v))
    return dict(columns)

def get_nested_value(d, key):
    
    if '.' not in key:
        if key not in d:
            return None
        return d[key]
    base_key, sub_key = key.split('.', 1)
    if base_key not in d:
        return None
    sub_dict = d[base_key]
    return get_nested_value(sub_dict, sub_key)

def get_row(json_lines, columns):
    """Returns csv file """
    row = []
    for column_name in columns:
        line_value = get_nested_value(
                        json_lines,
                        column_name,
                        )
        if isinstance(line_value, str):
            row.append('{0}'.format(line_value.encode('utf-8')))
        elif line_value is not None:
            row.append('{0}'.format(line_value))
        else:
            row.append('')
    return row

'''def __unwrap(json_lines):
    return wrap(json_lines, width=len(json_lines))'''
 
if __name__ == '__main__':
    """Convert a  file from json to csv."""

    parser = argparse.ArgumentParser(
            description='Converting to CSV files',
            )

    parser.add_argument(
            'json_file',
            type=str,
            help='The json file to convert into CSV for the project.',
            )

    args = parser.parse_args()

    json_file = args.json_file
    csv_file = '{0}.csv'.format(json_file.split('.json')[0])

    columns = get_superset_of_columns_from_file(json_file)
    read_write_file(json_file, csv_file, columns)
