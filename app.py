import logging
import sys
from collections import ChainMap
from PyQt5.QtWidgets import QApplication

from src.services.InfoMoney import InfomoneyStrategy
from src.gui.main_window import MainWindow, LoadingWindow

def all_stock_data_url() -> dict:
    file_path = "src/resources/stock_list.txt"
    with open(file_path) as file:
        return [url.rstrip() for url in file]

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(message)s', datefmt='%m-%d-%Y %I:%M:%S %p')
    app = QApplication(sys.argv)
    loading_window = LoadingWindow()
    loading_window.show()

    stock_strategy = InfomoneyStrategy()
    stock_info = []
    for url in all_stock_data_url():
        stock_strategy.get_info(url)
        stock_value = stock_strategy.to_dict()
        if not stock_value:
            continue
        stock_info.append(stock_value)

    headers = ['name', 'open', 'previous_close', 'minimal', 'maximum', 'month_variation', 'day_variation', 'year_variation', 'variation_52_weeks', 'volume', 'business_volume']
    loading_window.close()
    print(stock_value)
    window = MainWindow(stock_info, headers)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()