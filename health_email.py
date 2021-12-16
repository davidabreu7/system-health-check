import smtplib
def send_email(body=""):
    from_add = "me@email"
    to_add = "you@email"
    smtp_server = smtplib.SMTP("smtp.sever", 587)
    smtp_server.ehlo()
    # smtp_server.starttls()
    # smtp_server.login("david.abreu@mpf.mp.br")
    smtp_server.sendmail(from_add, to_add, body)
    smtp_server.quit()
