from selenium import webdriver

url = 'https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten?numberofrooms=-3.5&price=-950.0&exclusioncriteria=swapflat&pricetype=calculatedtotalrent&geocodes=1100000001,1100000003,110000000201&sorting=2'

#driver = webdriver.Firefox()
driver = webdriver.Safari()
driver.get(url)
print(driver)