from dotenv import load_dotenv
import os, sys
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def read_ss_list(file_name):
    """Read the Secret Santa Participants Text File (System Argument in main())

    Args:
        file_name [str]: file path/name of the text file that contains names and email of the secret santa participants

    Returns:
        people_dict [dict]: Python dictionary of people participating in Secret Santa with names as keys and emails as values
    """
    # READ IN PEOPLE FILE
    people = open(file_name).readlines()
    people = [person.strip('\n') for person in people]

    # SPLIT INTO DICTIONARY KEY == NAME | EMAIL == VALUES
    people_dict = {}
    for person in people:
        name = person.split(',')[0]
        email = person.split(',')[1]
        people_dict[name] = email
    
    # RETURN PEOPLE_DICTIONARY
    return people_dict

def secret_santa(participants_dict):
    """Generate partners for Secret Santa

    Args:
        participants_dict [dict]: Python dictionary of people participating in Secret Santa with names as keys and emails as values

    Returns:
        list: Returns a list of tuples, with each tuple representing the partners for Secret Santa
    """
    # GET NAMES OF EVERYONE INVOLVED
    names = list(participants_dict.keys())

    # RANDOMLY SELECT TWO PEOPLE FROM THE LIST, SAVE THE PARTNERS, AND KEEP GOING UNTIL THERE IS NO ONE LEFT
    partners_list = []
    for i in range(int(len(names)/2)):
        partners = random.sample(names, 2)
        names = list(set(names) - set(partners))
        partners_list.append(tuple(partners))
    
    # RETURN PARTNERS LIST
    return partners_list

def email_participants(people_dictionary, partners_list, path_to_template):
    """Email each participant who they have for Secret Santa

    Args:
        people_dictionary [dict]: Python dictionary with each item being a name : email key-value pair
        partners_list [list]: List of tuples, with each tuple representing the partners for Secret Santa 
        path_to_template [str]: File name/path to the templated body of the email to be sent -- placeholders should be marked with {}
    """
    # READ IN THE EMAIL TEMPLATE
    ss_template = open(path_to_template).read()
    
    # ITERATE THROUGH PARTNER LIST AND SEND EMAILS
    for person1, person2 in partners_list:
        # SENDING PERSON 1 EMAILS
        
        # FORMAT THE TEMPLATE MESSAGE 
        ss_filled = ss_template.format(person1, person2)
        
        # GET EMAIL AND PASSWORD TO SEND OUT THE MESSAGES
        load_dotenv() # YOU'LL NEED TO CONFIGURE A .env FILE THAT CONTAINS THE BELOW VARIABLES WITH RESPECTIVE VALUES
        sender_email = os.environ.get('sender_address')
        sender_pass = os.environ.get('sender_pass')
        
        # SET UP THE MIME sets up the MIME
        message = MIMEMultipart()
        message['From'] = sender_email # MY EMAIL ADDRESS | FROM ME
        message['To'] =  people_dictionary[person2] # RECEIVER OF EMAIL | TO YOU
        message['Subject'] = 'Secret Santa 2022' # SUBJECT OF THE EMAIL
        
        # SET THE BODY OF THE EMAIL
        message.attach(MIMEText(ss_filled, 'plain'))

        # CREATE THE SMTP SESSION FOR SENDING THE EMAILScreates the SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.connect("smtp.gmail.com", 587)
        session.ehlo()
        session.starttls()
        session.login(sender_email, sender_pass)
        text = message.as_string()
        session.sendmail(sender_email, people_dictionary[person2], text)
        
        # SENDING PERSON 2 EMAILS
        
        # FORMAT THE TEMPLATE MESSAGE 
        ss_filled = ss_template.format(person2, person1)
        
        # GET EMAIL AND PASSWORD TO SEND OUT THE MESSAGES
        load_dotenv() # YOU'LL NEED TO CONFIGURE A .env FILE THAT CONTAINS THE BELOW VARIABLES WITH RESPECTIVE VALUES
        sender_email = os.environ.get('sender_address')
        sender_pass = os.environ.get('sender_pass')
        
        # SET UP THE MIME sets up the MIME
        message = MIMEMultipart()
        message['From'] = sender_email # MY EMAIL ADDRESS | FROM ME
        message['To'] =  people_dictionary[person1] # RECEIVER OF EMAIL | TO YOU
        message['Subject'] = 'Secret Santa 2022' # SUBJECT OF THE EMAIL
        
        # SET THE BODY OF THE EMAIL
        message.attach(MIMEText(ss_filled, 'plain'))

        # CREATE THE SMTP SESSION FOR SENDING THE EMAILScreates the SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.connect("smtp.gmail.com", 587)
        session.ehlo()
        session.starttls()
        session.login(sender_email, sender_pass)
        text = message.as_string()
        session.sendmail(sender_email, people_dictionary[person1], text)
        session.quit()
            
if __name__ == "__main__":
    approval_status = "NOT APPROVED"
    while approval_status == "NOT APPROVED":
        people_email_dict = read_ss_list(str(sys.argv[1]))
        partners = secret_santa(people_email_dict)
        print(partners)
        approval = input("PLEASE APPROVE THE ABOVE SECRET SANTA PAIRINGS: ")
        if approval == 'APPROVED':
            email_participants(people_email_dict, partners, "secret_santa_template.txt")
            approval_status = "APPROVED"
        else:
            approval_status = "NOT APPROVED"
