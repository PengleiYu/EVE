import pandas as pd
import numpy as np
from typing import List

volum = pd.Series({
    "ice_ship": 9000,
    "ice_per_second": 11,
    "ice_per_second_with_drug": 16.4,
    #     "ice_per_second_with_drug":27,
    "mine_ship": 31625,
    "mine_per_second": 7.5,
    "mine_per_second_with_drug": 10.1,
})


def format_money(money: int) -> str:
    return "{:.2f}W".format(money / 10000)


def create_df(list: List) -> pd.DataFrame:
    df = pd.DataFrame(list, columns=['name', 'total_value', 'volum', 'ice'])
    df = df.set_index('name')
    return df


def process_df(df: pd.DataFrame) -> pd.DataFrame:
    _value_per_cube = df['total_value'] / df['volum']
    _volum_of_ship = np.where(df['ice'], volum.ice_ship, volum.mine_ship)
    _volum_per_second = np.where(df['ice'], volum.ice_per_second, volum.mine_per_second)
    _volum_per_second_with_drug = np.where(df['ice'], volum.ice_per_second_with_drug, volum.mine_per_second_with_drug)

    # 每船价值
    _value_per_ship = _volum_of_ship * _value_per_cube
    # 每小时价值
    _value_per_hour = 2 * _volum_per_second * 3600 * _value_per_cube
    # 嗑药每小时价值
    _value_per_hour_with_drug = 2 * _volum_per_second_with_drug * 3600 * _value_per_cube

    result = pd.DataFrame({
        'ice': df['ice'],
        '嗑药money/h': _value_per_hour_with_drug,
        'money/h': _value_per_hour,
        'money/船': _value_per_ship,
        "money/m3": _value_per_cube,
        "满船min": _volum_of_ship / _volum_per_second / 60 / 2,
        "嗑药满船min": _volum_of_ship / _volum_per_second_with_drug / 60 / 2,
    }, )

    return result.sort_values(result.columns[1])
