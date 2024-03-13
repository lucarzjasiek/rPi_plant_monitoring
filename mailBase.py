import umail

'''W poniższych zmiennych należy umieścić odpowiednio email nadawcy (sender_email),
                                                       nazwę nadawcy, którą chcemy wyświetlać (sender_name),
                                                       hasło aplikacji pobierane ze odpowiednej strony usług google (chodzi tutaj o dokladnie: app password gmail) (sender_app_password),
                                                       email odbiorcy (recipient_email)
                                                       temat maila (email_subject)'''
sender_email = "twoj_email@poczta.com"
sender_name = "Wyświetlana nazwa nadawcy"
sender_app_password = "haslo dla aplikacji gmail"
recipient_email = "email_odbiorcy@poczta.com"  # variable
email_subject = "tytuł maila"  # variable

def SendMail(sender_email,sender_name,sender_app_password, recipient_email, email_subject):
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)
    smtp.login(sender_email, sender_app_password)
    smtp.to(recipient_email)
    smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
    smtp.write("Subject:" + email_subject + "\n")
    smtp.write("This is an email from Raspberry Pi Pico") #przykładowa treść maila
    smtp.send()
    smtp.quit()