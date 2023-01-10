from selenium import webdriver
import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path="chromedriver.exe")
url = "https:\\www.ccilindia.com/OMMWSG.aspx"
driver.get(url)

time.sleep(2)

# This dictionary will hold all the data for each page.
row_info = {}

def next_page(page):
    if page == 1:
        next_page = driver.find_element(By.XPATH,"/html/body/form/table[5]/tbody/tr[1]/td/table/tbody/tr[27]/td/a[1]")
    elif page == 2:
        print("Moving to last page")
        next_page = driver.find_element(By.XPATH,"/html/body/form/table[5]/tbody/tr[1]/td/table/tbody/tr[27]/td/a[2]")
    else:
        print("Last page reached, closing...")
        return None
    webdriver.ActionChains(driver).move_to_element(next_page).click().perform()


for page in range(1,4):
    print("Current page:", page)

    # After trial and error,
    # I found that these elements contain all the required data in a single page
    table_row = driver.find_elements(By.TAG_NAME,"tr")[5]
    td = table_row.find_elements(By.TAG_NAME,"td")[0].text
    print(td)

    # Creates a dictionary Key for current page and adds table data as Value
    row_info[f"page_{page}"] = td

    time.sleep(2)
    next_page(page)
    time.sleep(2)

print("---")
print(row_info["page_1"])
print("---")
print(row_info["page_2"])
print("---")
print(row_info["page_3"])

driver.close()