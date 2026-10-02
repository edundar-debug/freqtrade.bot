# Freqtrade Bot Sandbox

Mein persönliches Lernprojekt, um algorithmische Handelsstrategien mit [Freqtrade](https://www.freqtrade.io) zu entwickeln und lokal zu backtesten. Es wird **nur im Dry-Run / Backtest** gearbeitet, es ist kein echtes Geld im Spiel und keine Anlageberatung.

## Worum geht es hier?
Dieses Repository dient mir als Lernumgebung, um den automatisierten Krypto-Handel zu verstehen. Ich teste verschiedene Indikatoren, Parameter und Konfigurationen und schaue, wie sich Strategien unter historischen Marktdaten verhalten.

## Struktur
- `config.json.example`: Vorlage für die Bot-Konfiguration. Kopieren nach `config.json` und lokal anpassen. `config.json` selbst ist in `.gitignore` und wird nie hochgeladen (Secrets).
- `user_data/strategies/MyFirstStrategy.py`: unveränderte Freqtrade-Vorlage (Ausgangspunkt, nicht getestet).
- `user_data/strategies/MyFirstStrategyV1.py`: meine angepasste Strategie (Stoploss -3 %, Trailing-Stop, eigene ROI-Tabelle).
- `user_data/strategies/MyFirstStrategyV2.py`: wie V1, aber mit neuer ROI-Tabelle.
- `results/`: Backtest-Vergleich V1 gegen V2 (`BACKTEST_VERGLEICH.md`) und alle Trades als CSV.

## Backtest ausführen
Freqtrade ist nicht Teil dieses Repos und muss separat installiert sein ([Anleitung](https://www.freqtrade.io/en/stable/installation/)).

```bash
cp config.json.example config.json
freqtrade download-data -c config.json --timeframes 5m --timerange 20241001-
freqtrade backtesting -c config.json --strategy MyFirstStrategyV1 --timerange 20241001-20250930
```

Achtung: Steht `minimal_roi`, `stoploss` oder `trailing_stop` in `config.json`, überschreibt das die Werte in der Strategie-Datei.

## Tech Stack
- **Framework:** Freqtrade (Python)
- **Version Control:** Git & GitHub
- **Environment:** macOS / VS Code

---

# Freqtrade Bot Sandbox (English)

A personal learning project to develop and locally backtest algorithmic trading strategies with [Freqtrade](https://www.freqtrade.io). Everything runs in dry-run / backtest mode only: no real money, no financial advice.

## What is this?
I created this repository as a learning playground to explore automated crypto trading. It helps me test indicators, parameters and configurations against historical market data.

## Project Structure
- `config.json.example`: configuration template. Copy to `config.json` and edit locally. `config.json` is git-ignored and never uploaded (secrets).
- `user_data/strategies/MyFirstStrategy.py`: unmodified Freqtrade template (starting point, not tested).
- `user_data/strategies/MyFirstStrategyV1.py`: my customized strategy (stoploss -3 %, trailing stop, own ROI table).
- `user_data/strategies/MyFirstStrategyV2.py`: same as V1 with a new ROI table.
- `results/`: V1 vs V2 backtest comparison (`BACKTEST_VERGLEICH.md`) and all trades as CSV.

## Running a backtest
Freqtrade is not part of this repo and must be installed separately. See the commands in the German section above.

Note: `minimal_roi`, `stoploss` or `trailing_stop` in `config.json` override the values in the strategy file.

## Tech Stack
- **Framework:** Freqtrade (Python)
- **Version Control:** Git & GitHub
- **Environment:** macOS / VS Code
