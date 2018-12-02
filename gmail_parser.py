#!/anaconda3/bin/python
import sys
import imaplib
import email
import email.header
import datetime
from connect import ConnectDB


EMAIL_ACCOUNT = "sx@gmail.com"
EMAIL_FOLDER = "text"
FILE_PATH = "/Users/tonys/PycharmProjects/manca"
BATCH_FILE = "/Users/tonys/PycharmProjects/manca/batch_number.txt"
CLIST = ['Q101','Q102','Q103','Q104','Q105','Q106','Q107','Q108','Q109','Q110','Q111']

class GmailParser:
    def __init__(self):
        self.db = ConnectDB()

    def get_msg_body(self, msg):
        split_string = "<https://voice.google.com>"
        strip_string = "YOUR ACCOUNT"
        new_user_msg = "To respond to this text message, reply to this email or visit Google Voice."
        msg_body = msg.get_payload()[0].get_payload()
        message = msg_body.split(split_string)[1].replace(strip_string,"").strip().replace(new_user_msg,"").strip()
        return message


    def calc_batch_number(self, BATCH_FILE):
        with open (BATCH_FILE,'r') as fr:
            batch_number = fr.read()
            if not batch_number:
                print ("ERROR getting batch number")
                return 0
            else:
                return int(batch_number)+1


    def write_batch_number(self, BATCH_FILE, current_batch_id):
        try:
            fw= open(BATCH_FILE,"w+")
            fw.write(str(current_batch_id))
            fw.close()
        except:
            print('Unable to open path specified for batch file')

    def calculate_mark(self, data):
        msg = email.message_from_string(data[0][1].decode("utf-8"))
        received_date = email.utils.parsedate_tz(msg['Date'])
        received_datetime = datetime.datetime.fromtimestamp(email.utils.mktime_tz(received_date))
        # check if the message is in vaid format
        msg_body = self.get_msg_body(msg).strip().upper()
        if msg_body not in CLIST:
            print("Invalid chest number",msg_body)
            return 'Q999',received_datetime
        # contestant_name = msg_body[0]
        # contestant_mark = int(msg_body[1])
        #
        # # do not assign mark if its below median or above boundary
        # if contestant_mark < 6 or contestant_mark > 10:
        #     print("Invalid mark range ",msg_body)
        #     return 'unknown',contestant_mark,received_datetime
        return msg_body, received_datetime


    def calculate_received_from(self, data):
        subject = str(data[0]).split("Subject: New text message from")[1][:15].strip()
        received_from = subject.strip("New text message from ")
        if len(received_from) != 0:
            return received_from
        else:
            return 'unknown'


    def process_mailbox(self, data,GMAIL):
        cur_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        current_batch_id = self.calc_batch_number(BATCH_FILE)
        print ("Processing batch is: ",current_batch_id)
        with open("quiz_answers"+"_"+cur_time+".txt", "w") as file_out:
            for num in data[0].split():
                rv, data = GMAIL.fetch(num, '(RFC822)')
                if rv != 'OK':
                    print ("ERROR getting message", num)
                    return
                sequence_id = int(num)
                contestant_name, received_time = self.calculate_mark(data)
                sender = self.calculate_received_from(data)
                file_out.write("%d\t%d\t%s\t%s\t%s\n" % (current_batch_id, sequence_id, sender, contestant_name, received_time))
                query = "insert into manca.queen_voting values(%d,%d,'%s','%s','%s')" % (current_batch_id, sequence_id, sender, contestant_name, received_time)
                print(query)
                self.db.insert(query)
        file_out.close()
        self.write_batch_number(BATCH_FILE, current_batch_id)


    def check_mailbox(self, GMAIL):
        rv, data = GMAIL.search(None, "UNSEEN")
        if rv != 'OK' or len(data[0].strip()) == 0:
            print ("\nNo messages found!")
        else:
            self.process_mailbox(data,GMAIL)
            return


    def Login_to_account(self):
            EXTRAP = 'xxxx'
            GMAIL = imaplib.IMAP4_SSL('imap.gmail.com')
            try:
                GMAIL.login(EMAIL_ACCOUNT,EXTRAP)
            except imaplib.IMAP4.error:
                print ("LOGIN FAILED!!! ")
                sys.exit(1)
            rv, data = GMAIL.select(EMAIL_FOLDER)
            if rv == 'OK':
                print ("\nJob is Parsing the emails from gmail folder 'text'")
                self.check_mailbox(GMAIL)
                GMAIL.close()
            else:
                print ("ERROR: Unable to open mailbox ", rv)
            GMAIL.logout()


if __name__=="__main__":
    # import pdb;pdb.set_trace()
    gmail_parser_obj = GmailParser()
    gmail_parser_obj.Login_to_account()
    print("\nJob completed successfully. Please check the results under the project directory")
    exit(0)
