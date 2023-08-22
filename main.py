from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

def input_details():
    current_day = int(input(f'What day is it today? (Enter a number): '))
    number_of_players = int(input(f'How many golfers? (Enter a number): '))
    return current_day, number_of_players

def initiate_driver():
    driver = webdriver.Chrome()
    driver.get("https://golfburnaby.cps.golf/onlineresweb/search-teetime?TeeOffTimeMin=0&TeeOffTimeMax=23")
    
    driver.maximize_window()
    
    return driver

def set_options(current_day, num_players, driver):
    wait = WebDriverWait(driver, 60)
    earliest_day = current_day + 5
    day_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "day-unit")))
    for day_element in day_elements:
        day_number = int(day_element.text)
        try:
            if day_number == earliest_day:
                try:
                # Click on the day element
                    print("Clicking on day:", day_number)
                    driver.execute_script("arguments[0].click()", day_element)
                    break
                except StaleElementReferenceException:
                    print("Retrying")
                    continue
        except StaleElementReferenceException:
            print("some shit")
            continue

    # For mobile view
    # form_element = wait.until(EC.element_to_be_clickable((By.XPATH, f'/html/body/app-root/app-full-layout/div/mat-sidenav-container/mat-sidenav-content/div[1]/app-search-teetime-page/div/div[1]/app-search-teetime-filters/div/div/div[3]/div[2]/mat-form-field/div/div[1]/div[2]/span/label/mat-label'))) 
    # driver.execute_script("arguments[0].click();", form_element)

    input("Press Enter to close the browser window...")

    driver.quit()

def main():
    current_day, number_of_players = input_details()
    driver = initiate_driver()
    time.sleep(2)
    set_options(current_day, number_of_players, driver)

if __name__ == "__main__":
    main()