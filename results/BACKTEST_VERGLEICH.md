# Backtest-Vergleich: V1 gegen V2 (neue ROI-Tabelle)

> Lernprojekt, keine Anlageberatung. Backtests bilden die Vergangenheit ab. Ausgeführt am 01.10.2026.

## Was geändert wurde
Nur die ROI-Tabelle. Alles andere in `MyFirstStrategyV2.py` ist identisch mit `MyFirstStrategyV1.py`.

**Hinweis:** `MyFirstStrategyV1.py` ist die lokal angepasste Version, die ich getestet habe (Stoploss -3 %, Trailing-Stop, eigene ROI-Tabelle). Die Datei `MyFirstStrategy.py` im Repo ist dagegen noch die unveränderte Freqtrade-Vorlage mit anderen Werten und wurde hier nicht getestet. V1 unterscheidet sich von ihr im Klassennamen und in den angepassten Werten (Stoploss, Trailing-Stop, ROI-Tabelle).

| Haltedauer | V1: Mindestgewinn | V2: Mindestgewinn |
| --- | --- | --- |
| ab 0 Minuten | 3 % | 4 % |
| ab 20 Minuten | 15 % | – |
| ab 40 Minuten | 8 % | – |
| ab 2 Stunden | – | 2,5 % |
| ab 6 Stunden | – | 1,5 % |
| ab 12 Stunden | – | 0,5 % |

## Aufbau
BTC/USDT und ETH/USDT, 5-Minuten-Kerzen von Binance (öffentliches Archiv, keine Lücken), Gebühr 0,1 % pro Order, 100 USDT pro Trade, max. 2 offene Trades, Startkapital 1.000 USDT. Zwei Zeiträume: A (Okt 2024 bis Sep 2025, Markt stieg) und B (Okt 2025 bis Aug 2026, Markt fiel).

## Ergebnisse
| Strategie | Zeitraum | Markt | Trades | Ergebnis | Gewinnquote | Ø Gewinn | Ø Verlust | nötige Quote | Max. Drawdown |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V1 | A | +70,6 % | 505 | -18,45 % | 56,0 % | +1,85 % | -3,19 % | 63,3 % | 20,1 % |
| V2 | A | +70,6 % | 630 | -20,76 % | 66,3 % | +1,12 % | -3,19 % | 74,0 % | 22,7 % |
| V1 | B | -36,8 % | 457 | -22,97 % | 54,7 % | +1,72 % | -3,19 % | 65,0 % | 25,5 % |
| V2 | B | -36,8 % | 569 | -21,82 % | 67,0 % | +1,00 % | -3,19 % | 76,1 % | 23,6 % |

„Nötige Quote" = Anteil gewonnener Trades, ab dem die Strategie ausgeglichen wäre, berechnet aus Ø Gewinn und Ø Verlust (die Prozentwerte enthalten die Gebühren bereits).

## Erkenntnisse
- **Die neue ROI-Tabelle hat das Problem nicht gelöst.** Die Gewinnquote stieg auf rund 67 %, aber die Gewinne wurden kleiner (ca. 1 %), und der Verlust blieb bei 3,19 %. Dadurch stieg die nötige Quote sogar auf 74 bis 76 %.
- **Die Strategie verliert auch in einem steigenden Markt** (Zeitraum A, Markt +70,6 %). Meine frühere Vermutung, sie scheitere vor allem im Abwärtstrend, stimmt so nicht.
- **Das Kernproblem ist das Verhältnis Gewinn zu Verlust.** Der Stoploss kostet ca. 3,2 % pro Fehltrade, die Gewinne liegen bei 1 bis 2 %.
- **Gebühren** liegen bei 91 bis 126 USDT pro Lauf und sind mehr als ein Drittel des Verlusts. Mehr Trades bedeuten mehr Gebühren.

## Wichtig beim Ändern der Strategie
Werte in `config.json` (zum Beispiel `minimal_roi`, `stoploss`, `trailing_stop`) überschreiben die gleichnamigen Werte in der Strategie-Datei. Wer die Strategie ändert, muss sie in der Config entfernen oder anpassen, sonst bleibt die Änderung ohne Wirkung.

## Dateien
- `user_data/strategies/MyFirstStrategyV1.py`: die getestete lokale Ausgangsversion (Basis für den Vergleich)
- `user_data/strategies/MyFirstStrategyV2.py`: Variante mit neuer ROI-Tabelle
- `results/trades_v1_zeitraumA.csv`, `trades_v1_zeitraumB.csv`: alle Trades von V1
- `results/trades_v2_zeitraumA.csv`, `trades_v2_zeitraumB.csv`: alle Trades von V2
