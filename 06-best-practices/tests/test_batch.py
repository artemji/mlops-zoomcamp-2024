import pytest
import pandas as pd
from datetime import datetime
from batch import prepare_data


def dt(hour, minute, second=0):
    """Create a datetime object for 2023-01-01 with specified time."""
    return datetime(2023, 1, 1, hour, minute, second)


def test_prepare_data():
    # Test data setup
    test_data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2), dt(1, 2, 59)),
        (3, 4, dt(1, 2), dt(2, 2, 1)),
    ]
    columns = ['PULocationID', 'DOLocationID',
               'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(test_data, columns=columns)

    # Columns to be treated as categorical
    categorical_columns = ['PULocationID', 'DOLocationID']
    processed_df = prepare_data(df, categorical_columns)

    # Expected results
    expected_results = [
        {'PULocationID': '-1', 'DOLocationID': '-1', 'duration': 9.0},
        {'PULocationID': '1', 'DOLocationID': '1', 'duration': 8.0},
    ]
    expected_df = pd.DataFrame(expected_results)

    # Assertion to compare actual vs expected
    assert processed_df[categorical_columns + ['duration']
                        ].to_dict(orient='records') == expected_df.to_dict(orient='records')
