from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json


email_to = "receiver@domain.com"
attachments_path = "./Attachments/"
config_path = "./Config/config.json"
email_body_path = './Config/email_body.txt'


### 0. GET THE BASIC DATA ###
# 0.1. Login credentials and email subject
with open(config_path, 'r') as json_file:
    data = json.load(json_file)
    protonmail_username = data['protonmail_username']
    protonmail_password = data['protonmail_password']
    email_subject = data['email_subject']
    attach_files = True if data['attach_files'].lower() == "true" else False

# 0.2. Email body
with open(email_body_path, 'r', encoding='utf-8') as f:
    email_body = f.read()

# Open browser
driver = webdriver.Edge()
driver.maximize_window()

### 1. LOGIN ###
url = 'https://account.proton.me/login'
driver.get(url)

# Wait for the username field to be visible
username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 
                                    'username')))
username.send_keys(protonmail_username)

# Wait for the password field to be visible
password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 
                                    'password')))
password.send_keys(protonmail_password)

# Wait for the submit button to be clickable
submit = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, 
                                "//button[text()='Sign in']")))
submit.click()

### 2. CHOOSE PROTON MAIL ###
# Wait for the Proton Mail link to be visible and clickable
# Maybe we will have to choose Proton Mail or maybe we will immediately
# Be redirected to Proton Mail. Thus we use try|except
try:
    pm = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, 
                                        "//div[text()='Proton Mail']")))
    pm.click()
except:
    pass

### 3. NEW MESSAGE ###
# Wait for the 'New message' button to be clickable
new_message_button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, 
                                "//button[text()='New message']")))
new_message_button.click()

### 4. EMAIL TO ###
# Wait for the email input field to be visible and interactable
email_input = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 
                                    '[data-testid="composer:to"]')))
email_input.send_keys(email_to + '\n')

### 5. SUBJECT ###
# Wait for the subject input to be clickable
subject_input = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 
                                '[data-testid="composer:subject"]')))
subject_input.click()
subject_input.send_keys(email_subject)

### 6. BODY ###
iframe = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 
                                    '[data-testid="rooster-iframe"]')))
driver.switch_to.frame(iframe)

# Add the email_body using JavaScript so we can alter rooster-editor
script = f"""
    var editorDiv = document.getElementById('rooster-editor');
    if (editorDiv) {{
        // Delete the 'Sent by Protonmail'
        editorDiv.innerHTML = '';

        // Create the new div element
        var newDiv = document.createElement('div');
        newDiv.style.fontFamily = 'Arial, sans-serif';
        newDiv.style.fontSize = '14px';
        newDiv.innerHTML = '{email_body}';

        // Insert the new div as the first child of the rooster-editor
        editorDiv.insertBefore(newDiv, editorDiv.firstChild);
    }}
"""

driver.execute_script(script)


### 7. FILE ATTACHMENT ###
# Wwitch to default content since before we switched to iframe
driver.switch_to.default_content()


if attach_files:
    # import pyautogui to handle attachments
    import pyautogui
    # Wait for the attachment button to be clickable
    attach = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 
                                    '[data-testid="composer:attachment-button"]')))
    attach.click()
    
    # Wait for the pyautogui to appear
    sleep(1)
    # Get a list of all files in the document directory
    documents = os.listdir(attachments_path)
    # Get the absolute path of each document
    document_paths = [os.path.abspath(os.path.join(attachments_path, file)) for file in documents]
    # Add "" so we can join them and choose multiple documents
    document_paths = [f'"{path}"' for path in document_paths]
    # Join the documents
    all_files = ' '.join(document_paths)
    # Write to pyautogui
    pyautogui.write(all_files)
    # Enter and wait to upload
    pyautogui.press('enter')
    sleep(5)

### 8. SEND THE EMAIL ###
# Wait for the send button to be clickable
send_button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 
                                '[data-testid="composer:send-button"]')))
send_button.click()
# Give some time for the email to be sent
sleep(3)
# Close the webdriver
driver.quit()