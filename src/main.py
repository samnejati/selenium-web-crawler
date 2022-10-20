import pandas as pd 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from utils import store_data


service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get('https://coinmarketcap.com/currencies/bitcoin/historical-data/')


for i in range (2):
    button = driver.find_element(By.CSS_SELECTOR,"#__next > div > div.main-content > div.sc-4vztjb-0.cLXodu.cmc-body-wrapper > div > div.sc-1prm8qw-0.bUVslT.container > div > div > div.history > p:nth-child(3) > button")
    driver.execute_script("arguments[0].click();", button)  

col_names = driver.find_elements(By.CSS_SELECTOR, ".stickyTop")
col_names_text = [i.text for i in col_names]

rest_cols = []
for i in range(1,8):
    rest_col_list = driver.find_elements(By.CSS_SELECTOR, f"td:nth-child({i})") 
    col_list_text = [i.text for i in rest_col_list] 
    rest_cols.append(col_list_text)


df = pd.DataFrame(rest_cols ).T
df.columns = col_names_text


store_data('postgres', '1234', 'localhost', '5432', 'coinmarketcap', df, 'btc2')