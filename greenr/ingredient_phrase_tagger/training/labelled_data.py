import unicodecsv

_REQUIRED_COLUMNS = ['input', 'name', 'qty', 'range_end', 'unit', 'comment']


class Error(Exception):
    pass


class InvalidHeaderError(Error):
    pass


class Reader(object):
    """Reads labelled ingredient data formatted as a CSV.

    Input data must be a CSV file, encoded in UTF-8, and containing the
    following columns:

        input
        name
        qty
        range_end
        unit
        comment
    """

    def __init__(self, data_file):
        self._csv_reader = unicodecsv.DictReader(data_file)
        for required_column in _REQUIRED_COLUMNS:
            if required_column not in self._csv_reader.fieldnames:
                raise InvalidHeaderError(
                    'Data file is missing required column: %s' %
                    required_column)

    def __iter__(self):
        return self

    def next(self):
        return _parse_row(self._csv_reader.next())


def _parse_row(row):
    """Parses a row of raw data from a labelled ingredient CSV file.

    Args:
        row: A row of labelled ingredient data. This is modified in place so
            that any of its values that contain a number (e.g. "6.4") are
            converted to floats and the 'index' value is converted to an int.

    Returns:
        A dictionary representing the row's values, for example:

        {
            'input': '1/2 cup yellow cornmeal',
            'name': 'yellow cornmeal',
            'qty': 0.5,
            'range_end': 0.0,
            'unit': 'cup',
            'comment': '',
        }
    """
    # Certain rows have range_end set to empty.
    if row['range_end'] == '':
        range_end = 0.0
    else:
        range_end = float(row['range_end'])

    return {
        'input': row['input'],
        'name': row['name'],
        'qty': float(row['qty']),
        'range_end': range_end,
        'unit': row['unit'],
        'comment': row['comment'],
    }


class Writer(object):
    """Writes labelled ingredient data to a CSV file."""

    def __init__(self, data_file):
        self._csv_writer = unicodecsv.DictWriter(
            data_file, fieldnames=_REQUIRED_COLUMNS, lineterminator='\n')
        self._csv_writer.writeheader()

    def writerow(self, row):
        """Adds a row of data to the output CSV file.

        Args:
            row: A dictionary of values for a labelled ingredient. The
                dictionary must contain the following keys:

                * input
                * name
                * qty
                * range_end
                * unit
                * comment
        """
        self._csv_writer.writerow(row)

    def writerows(self, rows):
        """Writes multiple rows to the output CSV file."""
        self._csv_writer.writerows(rows)
