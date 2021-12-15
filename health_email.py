import smtplib
def send_email(body=""):
    from_add = "david.abreu@outlook.com"
    to_add = "david.abreu@outlook.com"
    smtp_server = smtplib.SMTP("smtp.office365.com", 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login("david.abreu@outlook.com", "password")
    smtp_server.sendmail(from_add, to_add, body)
    smtp_server.quit()
