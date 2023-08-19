from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

def input_details():
    current_day = int(input(f'What day is it today? (Enter a number): '))
    number_of_players = int(input(f'How many golfers? (Enter a number): '))
    return current_day, number_of_players

def initiate_driver(current_day, num_players):
    earliest_day = current_day + 5

    driver = webdriver.Chrome()
    driver.get("https://golfburnaby.cps.golf/onlineresweb/search-teetime?TeeOffTimeMin=0&TeeOffTimeMax=23")
    driver.implicitly_wait(30.0)

    wait = WebDriverWait(driver, 30)

    form_element = wait.until(EC.element_to_be_clickable((By.XPATH, f'/html/body/app-root/app-full-layout/div/mat-sidenav-container/mat-sidenav-content/div[1]/app-search-teetime-page/div/div[1]/app-search-teetime-filters/div/div/div[3]/div[2]/mat-form-field/div/div[1]/div[2]/span/label/mat-label'))) 
    driver.execute_script("arguments[0].click();", form_element)


    # NOT WORKING YET YAHOO
    for _ in range(35):
        try:
            day_elements = driver.find_elements(By.XPATH, "//span[contains(@class, 'day-unit')]")
            for day in day_elements:
                try:
                    day_value = day.find_element(By.CLASS_NAME, "day-background-upper")
                    if day_value.text == earliest_day:
                        driver.execute_script("arguments[0].click();", day_value)
                        break
                except StaleElementReferenceException:
                    continue
        except StaleElementReferenceException:
            continue

    # day_elements = driver.find_elements(By.XPATH, "//span[contains(@class, 'day-unit')]")
    # for day in day_elements:
    #     try:
    #         day_value = day.find_element(By.CLASS_NAME, "day-background-upper")
    #         print(day_value.text)
    #         if day_value.text == earliest_day:
    #             driver.execute_script("arguments[0].click();", day_value)
    #             break
    #     except StaleElementReferenceException:
    #         # Handle the stale element reference exception here, e.g., re-run the loop or refresh the page
    #         continue

    input("Press Enter to close the browser window...")

    driver.quit()

def main():
    current_day, number_of_players = input_details()
    initiate_driver(current_day, number_of_players)

if __name__ == "__main__":
    main()