import win32com.client

class Email:
    def __init__(self):
        outlook = win32com.client.Dispatch('outlook.application')
        self.mail = outlook.CreateItem(0)
        self.mail.To = 'williamcondron@live.ie'
        self.mail.Subject = 'Device Alert Email'
        self.mail.HTMLBody = '<h3>This is HTML Body</h3>'
        #mail.Attachments.Add('c:\\sample.xlsx')
        #mail.Attachments.Add('c:\\sample2.xlsx')
        #mail.CC = 'somebody@company.com'

    def send_email(self, target):
        self.mail.Body = f"This is your alert email. Device {target} was found on the network"
        self.mail.Send()
