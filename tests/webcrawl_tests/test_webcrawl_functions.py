import sys
import os
from webcrawl_functions import open_url


webcrawl_functions_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'PurduePrep', 'webcrawl'))
sys.path.insert(1, webcrawl_functions_path)


def test_open_url_good_link():
    test_url = 'https://weeklyjoys.wordpress.com/wp-content/uploads/2021/10/ece404_e1_sp2021.pdf'
    hex_content = open_url(test_url)
    assert hex_content.status_code == 200
