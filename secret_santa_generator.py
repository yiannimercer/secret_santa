from dotenv import load_dotenv
import os, sys
import numpy as np
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


def secret_santa(participants_dict, restrictions_set):
    """
    Generate partners for Secret Santa ensuring certain pairs are not matched together.

    Args:
        participants_dict [dict]: Python dictionary of people participating in Secret Santa with names as keys and emails as values
        restrictions_set [set]: A set of tuples containing pairs of names that cannot be paired together

    Returns:
        list: Returns a list of tuples, with each tuple representing the partners for Secret Santa
    """
    names = list(participants_dict.keys())
    result = []
    restart = True

    while restart:
        restart = False
        receivers = names[:]

        for i in range(len(names)):
            giver = names[i]
            possible_receivers = [receiver for receiver in receivers if receiver != giver and (giver, receiver) not in restrictions_set and (receiver, giver) not in restrictions_set]

            if not possible_receivers:
                restart = True
                break

            receiver = random.choice(possible_receivers)
            result.append((giver, receiver))
            receivers.remove(receiver)

    return result


def read_restrictions(file_name):
    """Read the restrictions for pairings from a text file.

    Args:
        file_name [str]: file path/name of the text file that contains restricted pairings

    Returns:
        set of tuples: A set of tuples, each containing a pair of names that cannot be paired together
    """
    restrictions = set()
    with open(file_name, 'r') as file:
        for line in file:
            pair = tuple(line.strip().split(','))
            restrictions.add(pair)
    return restrictions



def email_participants(people_dictionary, partners_list, email_subject):
    """Email each participant who they have for Secret Santa

    Args:
        people_dictionary [dict]: Python dictionary with each item being a name : email key-value pair
        partners_list [list]: List of tuples, with each tuple representing the partners for Secret Santa 
        email_subject [str]: The subject of the email being sent
    """
    # READ IN THE EMAIL TEMPLATE
    ss_template = open('secret_santa_template.txt').read()
    
    # ITERATE THROUGH PARTNER LIST AND SEND EMAILS
    for person1, person2 in partners_list:
        
        # FORMAT THE TEMPLATE MESSAGE 
        ss_filled = ss_template.format(person1, person2)
        
        # GET EMAIL AND PASSWORD TO SEND OUT THE MESSAGES
        load_dotenv() # YOU'LL NEED TO CONFIGURE A .env FILE THAT CONTAINS THE BELOW VARIABLES WITH RESPECTIVE VALUES
        sender_email = os.environ.get('sender_address')
        sender_pass = os.environ.get('sender_pass')
        
        # SET UP THE MIME sets up the MIME
        message = MIMEMultipart()
        message['From'] = sender_email # MY EMAIL ADDRESS | FROM ME
        message['To'] =  people_dictionary[person1] # RECEIVER OF EMAIL | TO YOU
        message['Subject'] = email_subject # SUBJECT OF THE EMAIL
        
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
