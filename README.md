# ProtonMail Automation Script

This Python script automates sending emails via ProtonMail using Selenium. Since ProtonMail does not offer free SMTP access, this script uses web automation to achieve the same result.

## Features
- Send automated emails from your ProtonMail account.
- Optional attachment handling with `pyautogui` for easy file uploads.

## Requirements
- **ProtonMail Account**
- **Selenium WebDriver** – Ensure compatibility with your browser.
- **pyautogui** – Only required if you want to include attachments in emails.

## Setup and Configuration

1. Clone this repository and install the required packages.
2. In `Config/config.json`, add your ProtonMail username and password:
   - `email_subject`: Define the subject line for the email.
   - `attach_files`: Set to `true` if you want to include attachments.
3. **Email Body**: Edit the email content in `Config/email_body.txt`.
4. **Attachments**: Place any files you wish to send in the `Attachments` folder.

### Example `config.json`:
```
{
  "username": "your_protonmail_username",
  "password": "your_protonmail_password",
  "email_subject": "Your Subject Here",
  "attach_files": "true"
}
```

## Usage
Run the script to send an email as configured. Attachments will be included if `attach_files` is set to `true` and there are files in the `Attachments` folder.
```bash 
python send_email.py
```

## Notes
- Ensure you have the correct WebDriver installed for your browser.
- The code doesn't handle captcha

Hope this script helps :)


