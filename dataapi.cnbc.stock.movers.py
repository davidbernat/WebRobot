from cloudnode import SwiftData, sd
from webrobot.core.WebRobot import WebRobot
from webrobot.parsing.utils import minify_soup, convert_tag_to_xpath
from webrobot.parsing.SoupHelpers import SoupHelpers
from webrobot.core.SeleniumHelpers import GE
from webrobot.parsing.solver import Solver, XNode
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import json

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Stock(SwiftData):
    ticker: sd.string()
    name: sd.string(analyze=True)
    price: sd.float()
    change: sd.float()
    note: sd.string(analyze=True)


# filename = "movers.html"
# with open(filename, "r") as f: html = f.read()
# soup = BeautifulSoup(html)
# soup = minify_soup(soup)
#
# components = ["SWKS", "Skyworks Solutions", "72.22", "7.904"]
# founds = [Solver.prune_to_leaves(Solver.find_text(soup, c)) for c in components]
# best = SoupHelpers.find_shared_parent_of_collections(founds)
# pruned = [[c for c in f if best in c.parents] for f in founds]
# convert_tag_to_xpath(best)
#
# names = ["ticker", "name", "price", "change"]
# rule = dict(
#     root=vars(XNode.from_tag(best)),
#     components={names[i]: vars(XNode.from_tag(p[0], get_attrs="__TEXT")) for i, p in enumerate(pruned)})
# rule["components"]["ticket"]["get_attrs"] = ["__TEXT", "href"]
# with open("dataapi.cnbc.stock.movers.rules.json", "w") as f: json.dump(rule, f)


# should add entry url and date and
with open("dataapi.cnbc.stock.movers.rules.json", "r") as f: rule = json.load(f)
root = XNode(**rule["root"])
components = {name: XNode(**c) for name, c in rule["components"].items()}

_buttons = ["S&P", "NASDAQ", "DOW"]
url = "https://www.cnbc.com/us-market-movers/"

def extract_cnbc_stock_movers():
    """an example of an api that returns swiftdata for cached cron repetitive database index creation"""
    driver = WebRobot.driver(headless=True)
    driver.get(url)

    buttons = WebDriverWait(driver, 10).until(
        lambda x: GE.wait_until_n_extracted(x, lambda x: GE.extract_buttons(x, _buttons), 3))

    data = dict()
    for i, button in enumerate(buttons):
        items = WebDriverWait(driver, 10).until(
            lambda x: GE.wait_until_n_extracted(x, lambda x: GE.extract_content(x, components, root=root), 24))
        # remove commas and % etc.
        for item in items: item["change"] = item["change"][0].replace(",", "").replace("%", "")
        for item in items: item["price"] = item["price"][0].replace(",", "").replace("%", "")
        items = [Stock.new(ticker=d["ticker"][0][0], name=d["name"][0], price=d["price"][0], change=d["change"]) for d in items]
        data[_buttons[i]] = items
    return data

if __name__ == "__main__":
    data = extract_cnbc_stock_movers()
    data = {key: [item.as_dict() for item in items] for key, items in data.items()}
    with open("dataapi.cnbc.stock.movers.data.json", "w") as f: json.dump(data, f)
