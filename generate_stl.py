"""
Text to STL Generator

This script uses Selenium to automate the process of generating STL files
from text using the website "https://text2stl.mestres.fr/en-us/generator".

Requirements:
    - Chrome WebDriver installed and added to PATH
    - Selenium package installed

To run this script:
    1. Ensure the necessary requirements are met.
    2. Update the names list with the names you want to convert.
    3. Run the script using `python generate_stl.py name1 name2 name3`.
"""

import os
import time
import argparse
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def generate_stl(name):
    """
    Generates an STL file from the provided name.

    :param name: The text name you want to convert into an STL file.
    """
    # Set up headless Chrome options
    options = Options()
    options.add_argument("--headless")

    # Create WebDriver instance
    driver = webdriver.Chrome(options=options)

    # Open the text to STL website
    driver.get("https://text2stl.mestres.fr/en-us/generator")

    # Create a wait instance with a 2-second timeout
    wait = WebDriverWait(driver, 2)

    # Find and fill the text box
    text_box = wait.until(EC.element_to_be_clickable((By.ID, "text-content")))
    text_box.clear()
    text_box.send_keys(name)

    # Find and select the shape
    shape_select = wait.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                'img[src="/img/type_1-ef2c7bc83976e176942a0ba5f7e76251.png"]',
            )
        )
    )
    shape_select.click()

    # Find and set the height
    height_box = wait.until(EC.element_to_be_clickable((By.ID, "text-height")))
    height_box.clear()
    height_box.send_keys("5")

    # Find and set the kerning
    kerning_box = wait.until(EC.element_to_be_clickable((By.ID, "text-spacing")))
    kerning_box.clear()
    kerning_box.send_keys("0")

    # Find and click the font button
    font_button = driver.find_element(By.LINK_TEXT, "FONT")
    font_button.click()

    # Find and click the custom font checkbox
    custom_font = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[data-test-custom-checkbox]")
        )
    )
    custom_font.click()
    time.sleep(0.5)  # Give a little extra time for the file input to appear

    # Find the label element and its associated input element to select the font file
    label_element = driver.find_element(
        By.CSS_SELECTOR, "label[data-test-input-label='']"
    )
    file_input_element_id = label_element.get_attribute("for")
    file_input_element = driver.find_element(By.ID, file_input_element_id)
    font_file = os.path.abspath("Countryside-YdKj.ttf")
    file_input_element.send_keys(font_file)

    # Find and click the export button
    export_button = driver.find_element(
        By.CSS_SELECTOR,
        'button.uk-button.uk-button-primary.uk-align-center[type="button"]',
    )
    export_button.click()

    # Wait for the download to finish and rename the file
    time.sleep(2)
    download_path = "output.stl"
    new_path = f"{name}.stl"
    os.rename(download_path, new_path)

    # Close the WebDriver instance
    driver.quit()


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Generate STL files from provided names."
    )
    parser.add_argument(
        "names", nargs="+", help="List of names to convert into STL files."
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    for name in tqdm(args.names, desc="Generating STL files"):
        generate_stl(name.lower())
