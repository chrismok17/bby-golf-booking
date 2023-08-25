from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from dotenv import load_dotenv
import configparser
import os, sys, time, datetime


def get_day():
    """
    Get the current day.

    Returns: day
    """
    date = datetime.date.today()
    current_day = date.day
    print(f"Today is {date}.")

    return current_day


def initiate_driver():
    """
    Initiate the Chrome browser in fullscreen mode.

    Returns: driver
    """
    driver = webdriver.Chrome()
    driver.get(
        "https://golfburnaby.cps.golf/onlineresweb/search-teetime?TeeOffTimeMin=0&TeeOffTimeMax=23"
    )
    wait = WebDriverWait(driver, 60)
    driver.maximize_window()

    return driver, wait


def click_day(current_day, driver, wait):
    """
    Takes the current day and clicks on the earliest clickable day element for booking with 4 players as the default.

    Outome: With the 4 players option selected and the earliest possible day clicked, times for that day should be visible
    """

    player_element = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//span[@class="mat-button-toggle-label-content" and text()="4"]/ancestor::button',
            )
        )
    )
    player_element.click()

    earliest_day = current_day + 5
    day_elements = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "day-unit"))
    )

    # Loop through each day element and check if the earliest possible day is the current element in the iteration
    # If it is then click on that day to see times
    for day_element in day_elements:
        day_number = int(day_element.text)
        try:
            if day_number == earliest_day:
                try:
                    print("Clicking on day:", day_number)
                    driver.execute_script("arguments[0].click()", day_element)
                    break
                except StaleElementReferenceException:
                    print("Retrying")
                    continue
        except StaleElementReferenceException:
            print("Retrying")
            continue


def click_time(wait):
    """
    Clicks the earliest available time element.

    Outcome: Clicks the earliest time available and takes user to login screen
    """
    try:
        time_elements = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "btnStepper"))
        )
        earliest_time = time_elements[0]
        earliest_time.click()
        print(f"Clicking on earliest day available...")
    except TimeoutException:
        print("Element not clickable within timeout")


def enter_email(wait):
    """
    This function enters the email and password found in the .env file

    Outcome: Email and password are submitted succesfully and are taken to the agreement and reservation page.
    """

    if getattr(sys, "frozen", False):
        # Executable
        config = configparser.ConfigParser()
        config.read("config.ini")
        email = config["Credentials"]["email"]
        password = config["Credentials"]["password"]
    else:
        # Dev Environment
        load_dotenv()
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")

    try:
        email_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@formcontrolname="email"]')
            )
        )
        email_input.send_keys(email)
        print(f"Entered email: {email}")

        submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
        )
        submit_button.click()

        password_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@formcontrolname="password"]')
            )
        )
        password_input.send_keys(password)

        sign_in_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
        )
        sign_in_button.click()
    except:
        print("Email not entered")


def confirm_reservation(driver, wait):
    """
    Clicks on the "next" button to continue to the reservation page and will confirm the tee time

    Outcome: The user should receive an email linked to their account about the tee time they have confirmed.
    """
    time.sleep(2)
    try:
        next_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CLASS_NAME,
                    "mat-focus-indicator.full-width.btn-action.mat-raised-button.mat-button-base.mat-primary",
                )
            )
        )
        next_button.click()

        finalize_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CLASS_NAME,
                    "mat-focus-indicator.large-button.button-continue.mat-flat-button.mat-button-base.mat-primary.ng-star-inserted",
                )
            )
        )
        finalize_button.click()
        print("Your reservation has been confirmed!")
        driver.quit()

    except:
        print("Unable to reserve.")


def main():
    current_day = get_day()
    driver, wait = initiate_driver()
    time.sleep(2)
    click_day(current_day, driver, wait)
    click_time(wait)
    enter_email(wait)
    confirm_reservation(driver, wait)


if __name__ == "__main__":
    main()
