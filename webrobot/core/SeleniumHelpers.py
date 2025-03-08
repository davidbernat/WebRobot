from webrobot.parsing.utils import minify_soup
from webrobot.parsing.solver import Solver, XNode
from bs4 import BeautifulSoup

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SlowlyScrollDownPage:
    # a very simple example of how slightly more realistic scrolling might be implemented inline using an AI
    # in general scrolling at maximum speed has not triggered website backends to restrict surfing due to robotics
    # one can also imagine how large databases of user engagement data, i.e., human CAPTCHA recordings or Firebase
    # Analytics or any software that directly records human mouse movements, could be used here instead as generative
    # AI to emulate countlessly realistic human actions. These models are fundamentally the same as natural language
    # generative AI; and the process of simulating from gathered data goes back decades in math (c.f. Monte Carlo).

    current_position = 0  # in units of y pixel
    n_small_scrolls_per_session = 10
    n_position_change_per_small_scroll = 300

    @staticmethod
    def slowly_scroll_down_page(_driver):
        total_available_height, scroll_i = _driver.execute_script("return document.body.scrollHeight"), 0
        while SlowlyScrollDownPage.current_position <= total_available_height \
                and scroll_i < SlowlyScrollDownPage.n_small_scrolls_per_session:
            SlowlyScrollDownPage.current_position += SlowlyScrollDownPage.n_position_change_per_small_scroll
            _driver.execute_script("window.scrollTo(0, {});".format(SlowlyScrollDownPage.current_position))
            logger.info(f"scroll y={SlowlyScrollDownPage.current_position}")
            total_available_height = _driver.execute_script("return document.body.scrollHeight")
            scroll_i += 1



class GE:

    @staticmethod
    def extract_content(_html, components, root=None):
        soup = BeautifulSoup(_html)
        soup = minify_soup(soup)
        blocks = [soup] if root is None else Solver.reduce_from_xnode(root).parse(soup)
        return [{name: Solver.reduce_from_xnode(c).parse(b) for name, c in components.items()} for b in blocks]

    @staticmethod
    def extract_buttons(_html, _buttons):
        soup = BeautifulSoup(_html)
        soup = minify_soup(soup)
        return [Solver.find_text(soup, button, is_button=True, exact=True, expect_one=True) for button in _buttons]

    @staticmethod
    def wait_until_n_extracted(_driver, function, n_expected):
        try:
            items = function(_driver.page_source)
            return items if len(items) >= n_expected else False
        except Exception as e:
            logger.error(f"wait_until_n_extracted.function failed error={e}")
            return False
