# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these imports ---
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from pandas import DataFrame
from typing import Dict, Optional, Union, Tuple

from freqtrade.strategy import (
    IStrategy,
    Trade,
    Order,
    PairLocks,
    informative,  # @informative decorator
    # Hyperopt Parameters
    BooleanParameter,
    CategoricalParameter,
    DecimalParameter,
    IntParameter,
    RealParameter,
    # timeframe helpers
    timeframe_to_minutes,
    timeframe_to_next_date,
    timeframe_to_prev_date,
    # Strategy helper functions
    merge_informative_pair,
    stoploss_from_absolute,
    stoploss_from_open,
    AnnotationType,
)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
from technical import qtpylib


class MyFirstStrategyV2(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = "5m"
    can_short: bool = False

    # ROI-Tabelle (Return on Investment): "Wenn ein Trade seit X Minuten offen ist
    # und mindestens Y Gewinn hat, verkaufe ihn."
    # Der Schlüssel ist die Haltedauer in Minuten, der Wert der Mindestgewinn (0.04 = 4 %).
    # Wichtig: Die Schwelle soll mit der Zeit SINKEN. Je länger ein Trade läuft,
    # desto eher nimmt man auch einen kleineren Gewinn mit, statt ewig zu warten.
    # (V1 hatte 3 % -> 15 % -> 8 %, also eine steigende Schwelle am Anfang.)
    minimal_roi = {
        "0": 0.04,     # sofort: ab 4 % Gewinn verkaufen
        "120": 0.025,  # nach 2 Stunden: ab 2,5 % verkaufen
        "360": 0.015,  # nach 6 Stunden: ab 1,5 % verkaufen
        "720": 0.005   # nach 12 Stunden: ab 0,5 % verkaufen (deckt Gebühren)
    }

    stoploss = -0.03
    trailing_stop = True
    trailing_only_offset_is_reached = True 
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02

    process_only_new_candles = True
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False
    startup_candle_count: int = 30

    buy_rsi = IntParameter(10, 40, default=30, space="buy")
    sell_rsi = IntParameter(60, 90, default=70, space="sell")

    order_types = {
        "entry": "limit",
        "exit": "limit",
        "stoploss": "market",
        "stoploss_on_exchange": False
    }

    order_time_in_force = {
        "entry": "GTC",
        "exit": "GTC"
    }

    @property
    def plot_config(self):
        return {
            "main_plot": {
                "tema": {},
                "sar": {"color": "white"},
            },
            "subplots": {
                "MACD": {
                    "macd": {"color": "blue"},
                    "macdsignal": {"color": "orange"},
                },
                "RSI": {
                    "rsi": {"color": "red"},
                }
            }
        }

    def informative_pairs(self):
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["adx"] = ta.ADX(dataframe)
        dataframe["rsi"] = ta.RSI(dataframe)
        stoch_fast = ta.STOCHF(dataframe)
        dataframe["fastd"] = stoch_fast["fastd"]
        dataframe["fastk"] = stoch_fast["fastk"]
        macd = ta.MACD(dataframe)
        dataframe["macd"] = macd["macd"]
        dataframe["macdsignal"] = macd["macdsignal"]
        dataframe["macdhist"] = macd["macdhist"]
        dataframe["mfi"] = ta.MFI(dataframe)

        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe["bb_lowerband"] = bollinger["lower"]
        dataframe["bb_middleband"] = bollinger["mid"]
        dataframe["bb_upperband"] = bollinger["upper"]
        dataframe["bb_percent"] = (
            (dataframe["close"] - dataframe["bb_lowerband"]) /
            (dataframe["bb_upperband"] - dataframe["bb_lowerband"])
        )
        dataframe["bb_width"] = (
            (dataframe["bb_upperband"] - dataframe["bb_lowerband"]) / dataframe["bb_middleband"]
        )

        dataframe["sar"] = ta.SAR(dataframe)
        dataframe["tema"] = ta.TEMA(dataframe, timeperiod=9)

        hilbert = ta.HT_SINE(dataframe)
        dataframe["htsine"] = hilbert["sine"]
        dataframe["htleadsine"] = hilbert["leadsine"]

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe["rsi"], self.buy_rsi.value)) &  
                (dataframe["tema"] <= dataframe["bb_middleband"]) &  
                (dataframe["tema"] > dataframe["tema"].shift(1)) &  
                (dataframe["volume"] > 0)  
            ),
            "enter_long"] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe["rsi"], self.sell_rsi.value)) &  
                (dataframe["tema"] > dataframe["bb_middleband"]) &  
                (dataframe["tema"] < dataframe["tema"].shift(1)) &  
                (dataframe["volume"] > 0)  
            ),
            "exit_long"] = 1
        return dataframe