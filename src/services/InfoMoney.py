import requests
import logging

from bs4 import BeautifulSoup
from lxml import etree

from src.data.StockData import StockData
from src.exceptions.StockExceptions import NotFoundStockData, StockSearchException


class InfomoneyStrategy(StockData):
    URL = "https://www.infomoney.com.br/cotacoes/"

    def __init__(self) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/108.0.0.0 Safari/537.36"
        }

    def get_info(self, name: str):
        try:
            self.stock_type = name.split("/")[1]

            stock_url = self.URL + name
            logging.info(f"Pesquisando fundo {stock_url}")
            request = requests.get(stock_url, headers=self.headers)
            if request.status_code != 200:
                logging.error(f"Erro ao pesquisar fundo {stock_url}")
                raise NotFoundStockData(
                    f"Cannot find the requested stock data from infomoney, {stock_url}"
                )

            logging.info("Consulta de fundo realizada com sucesso, realizando parser")

            soup = BeautifulSoup(request.content, "html.parser")

            self.dom = etree.HTML(str(soup))
        except Exception as e:
            logging.error("erro ao consultar o fundo solicitado", e, stock_url)

    def to_dict(self):
        try:
            return {
                "name": self.stock_name,
                "open": self.value_open,
                "previous_close": self.previous_close,
                "minimal": self.minimal,
                "maximum": self.maximum,
                "month_variation": self.day_variation,
                "day_variation": self.day_variation,
                "year_variation": self.day_variation,
                "variation_52_weeks": self.variation_ft_weeks,
                "volume": self.volume,
                "business_volume": self.bss_volume,
            }
        except Exception as e:
            logging.error("erro ao formatar o fundo solicitado", e)
            return

    @property
    def stock_name(self):
        xpath = {
            "acao": "/html/body/div[4]/div/div[1]/div[1]/div/div[1]/h1",
            "fii": "/html/body/main/section/div/div/div[1]/div[1]/div/h1",
        }
        return self.dom.xpath(xpath[self.stock_type])[0].text

    @property
    def value_open(self):
        xpath = {
            "acao": "/html/body/div[4]/div/div[1]/div[1]/div/div[1]/h1",
            "fii": "/html/body/div[7]/div/div[1]/div[1]/div[1]/table[1]/tbody/tr[2]/td[2]",
        }
        return self.dom.xpath(
            "/html/body/main/section/div/div/div[4]/div[1]/div[1]/span[2]"
        )[0].text

    @property
    def previous_close(self):
        return self.dom.xpath(
            "/html/body/main/section/div/div/div[4]/div[1]/div[2]/span[2]"
        )[0].text

    @property
    def minimal(self):
        return self.dom.xpath(
            "/html/body/main/section/div/div/div[4]/div[1]/div[3]/span[2]"
        )[0].text

    @property
    def maximum(self):
        return self.dom.xpath(
            "/html/body/main/section/div/div/div[4]/div[1]/div[4]/span[2]"
        )[0].text

    @property
    def day_variation(self):
        return self.dom.xpath(
            "/html/body/main/section/div/div/div[4]/div[2]/div[1]/span[2]/text()"
        )[1].strip()

    @property
    def month_variation(self):
        return self.dom.xpath(
            "/html/body/main/section/div/div/div[4]/div[2]/div[2]/span[2]/text()"
        )[1].strip()

    @property
    def year_variation(self):
        return self.dom.xpath(
            "/html/body/main/section/div/div/div[4]/div[2]/div[3]/span[2]/i"
        )[1].strip()

    @property
    def variation_ft_weeks(self):
        return self.dom.xpath(
            "//html/body/main/section/div/div/div[4]/div[2]/div[4]/span[2]/i"
        )[0].text

    @property
    def volume(self):
        return self.dom.xpath(
            "/html/body/main/section/div/div/div[4]/div[3]/div[1]/span[2]"
        )[0].text

    @property
    def bss_volume(self):
        return self.dom.xpath(
            "/html/body/main/section/div/div/div[4]/div[3]/div[2]/span[2]"
        )[0].text
