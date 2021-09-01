import contact_book
import sort_file
import Noter
import pathlib
import sys
from pathlib import Path
import pickle
import difflib

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return f'Command {e} not found!!!'
        except ValueError as e:
            return e
        except IndexError as e:
            return f'Command not full!!'
    return inner

#in USE add contact
def com_add(name, phone, email = None, adress = None, birthday=None):
    if name.value in [key.value for key in list(contact_list.keys())]:
        raise ValueError(f'The new contact cannot be saved because the name "{name.value}" already exists. '
                         f'Please enter a different name.\n')

    record = contact_book.Record(name, email, adress, birthday) + phone
    contact_list.add_record(name, record)
    return f'New contact is saved: name "{name.value}", phone "{phone.value}",'\
        f'email "{email if email else "-"}",'\
        f'adress "{adress if adress else "-"}",'\
        f' date of birth "{birthday.value if birthday else "-"}".\n'

#in USE change number
def com_change(name, phone, new_phone):
    print(new_phone)
    if not name in [key.value for key in list(contact_list.keys())]:
        raise ValueError(
            f'Сontact by name "{name}" does not exist. Enter the correct name.\n')
    for nam, rec in contact_list.items():
        if nam.value == name:
            for ph in rec.phones:
                if ph.value == phone:
                    rec.change_phone(ph, new_phone)
                    return f'Saved a new phone number "{new_phone.value}" for a contact with the name "{name}".\n'
        else:
            raise ValueError(
                f'The contact "{name}" does not have a phone number {phone}.\n')

#in USE add number
def com_join(name, phone):
    if not name in [key.value for key in list(contact_list.keys())]:
        raise ValueError(
            f'Сontact with name "{name}" does not exist. Enter the correct name.\n')
    for nam, rec in contact_list.items():
        if nam.value == name:
            record = rec + phone
            contact_list.add_record(nam, record)
    print (f'A new phone number "{phone.value}" has been added for the contact with the name "{name}".\n')

#in USE delete number
def com_delete(name, phone):
    if not name in [key.value for key in list(contact_list.keys())]:
        raise ValueError(
            f'Сontact by name "{name}" does not exist. Enter the correct name.\n')
    for nam, rec in contact_list.items():
        if nam.value == name:
            for ph in rec.phones:
                if ph.value == phone:
                    rec.phones.remove(ph)
                    print(f'Delete phone number "{ph.value}" for a contact with the name "{name}".\n') 

#in USE show
def com_search(pattern):
    result = ''
    for nam, rec in contact_list.items():
        phone_list = [phone.value for phone in rec.phones]
        for p in phone_list:
            if p.find(pattern) != (-1) or nam.value.find(pattern) != (-1):
                result = f'name: {nam.value}, phone: {" ".join([phone.value for phone in rec.phones])}, ' \
                          f' email {rec.email.value if rec.email else "-"} ' \
                          f'adress {rec.adress.value if rec.adress else "-"} '  \
                          f'birthday {rec.birthday.value if rec.birthday else "-"}\n' 
    if not result:
        raise ValueError(f'No matches.\n')
    return result


#in USE show
def com_delete_contact(name):
    for nam, rec in contact_list.items():
        if nam.value == name:
            contact_list.data.pop(nam)
            serialized_lpist = contact_list.save_dumped_data()
    if not result:
        raise ValueError(f'No matches.\n')
    return result



#in USE new email/adress/birthday
def com_join_attribute (name, email = None, adress = None, birthday = None):
    if not name in [key.value for key in list(contact_list.keys())]:
        raise ValueError(
            f'Сontact with name "{name}" does not exist. Enter the correct name.\n')
    for nam, rec in contact_list.items():
        if nam.value == name:
            if email:
                rec.email = email
                contact_list.add_record(nam, rec)
                print (f'A new email "{email}" has been added for the contact with the name "{name}".\n')
            if adress:
                rec.adress = adress
                contact_list.add_record(nam, rec)
                print (f'A new adress "{adress}" has been added for the contact with the name "{name}".\n')
            if birthday:
                rec.birthday = birthday
                contact_list.add_record(nam, rec)
                print (f'A new birthday "{birthday}" has been added for the contact with the name "{name}".\n')

#in USE delete email/adress/birthday
def com_delete_attribute (name, email = None, adress = None, birthday = None):
    if not name in [key.value for key in list(contact_list.keys())]:
        raise ValueError(
            f'Сontact with name "{name}" does not exist. Enter the correct name.\n')
    for nam, rec in contact_list.items():
        if nam.value == name:
            if email:
                print (f'A email "{rec.email}" has been remove for the contact with the name "{name}".\n')
                rec.email = None
                contact_list.add_record(nam, rec)
                
            if adress:
                print (f'A adress "{rec.adress}" has been remove for the contact with the name "{name}".\n')
                rec.adress = None
                contact_list.add_record(nam, rec)
            if birthday:
                print (f'A birthday "{rec.birthday}" has been remove for the contact with the name "{name}".\n')
                rec.birthday = None
                contact_list.add_record(nam, rec)
                


@ input_error
def get_command_handler(user_input):  
    if user_input[:2] == ['contact', 'book']:
        pass  
    else:
        raise KeyError(user_input[0])

@ input_error

def signal_handler(signal, frame):
    contact_list.save_dumped_data()
    sys.exit(0)


if __name__ == '__main__':
    contact_list = contact_book.AddressBook()
    #serialized_lpist = contact_list.save_dumped_data()
    contact_list = contact_list.read_dumped_data()
    path = pathlib.Path('contact_list.txt')
    
    noter = Noter.Noter()   
    ######### for HELP 1 MAIN MENU
    commands = ["contact", "noter", "sort file", "exit"]
    prediction_experience = {}
    ####
    try:
        with open("experience.dat", "rb") as f:
            prediction_experience = pickle.load(f)
    except FileNotFoundError:
        prediction_experience = {}  
    ####
    while True:
        print ('Main menu')
        command = input ('Enter comand (contact, noter, sort file, exit): ')
        ####
        if not command in commands:
            answer = ""
            while answer != "y":
                if command in commands:
                    break
                for key, value in prediction_experience.items():
                    if command in key:
                        print(f"(d)Perhaps you mean {prediction_experience[key]}")
                        answer = str(input("Answer (Y/N): ")).lower()
                        if answer == "n":
                            command = str(input("Command input error, try again: ")).lower()
                        elif answer == "y":
                            command = prediction_experience[key]
                            break
                if not command in commands:
                    result = str(difflib.get_close_matches(command, commands, cutoff=0.1, n=1))[2:-2]
                    print(f"Perhaps you mean {result}")
                    answer = str(input("Answer (Y/N): ")).lower()
                    if answer == "n":
                        command = str(input("Command input error, try again: ")).lower()
                    elif answer == "y":
                        prediction_experience[command] = result
                        command = result
        ####   
        if command == 'contact': #CONTACT

            print ('Contact assistant')
            ######## for HELP 2 CONTACT 
            commands = ["add contact", "delete contact", 
            "show", "show all",
            "add number", "change number","delete number", 
            "new email", "delete email",
            "new adress", "delete adress",
            "new birthday", "delete birthday",
            "return"]
            prediction_experience = {}
            ####
            try:
                with open("experience.dat", "rb") as f:
                    prediction_experience = pickle.load(f)
            except FileNotFoundError:
                prediction_experience = {}  
            ####
            while True: #CONTACT COMAND
                command = str(input("Enter command :>> ")).lower()
                ####
                if not command in commands:
                    answer = ""
                    while answer != "y":
                        if command in commands:
                            break
                        for key, value in prediction_experience.items():
                            if command in key:
                                print(f"(d)Perhaps you mean {prediction_experience[key]}")
                                answer = str(input("Answer (Y/N): ")).lower()
                                if answer == "n":
                                    command = str(input("Command input error, try again: ")).lower()
                                elif answer == "y":
                                    command = prediction_experience[key]
                                    break
                        if not command in commands:
                            result = str(difflib.get_close_matches(command, commands, cutoff=0.1, n=1))[2:-2]
                            print(f"Perhaps you mean {result}")
                            answer = str(input("Answer (Y/N): ")).lower()
                            if answer == "n":
                                command = str(input("Command input error, try again: ")).lower()
                            elif answer == "y":
                                prediction_experience[command] = result
                                command = result
                ####
                if command == "add contact": # add contact
                    print("Creating a contact...")
                    while True:
                        name = input("Enter name:> \n").split()[0]
                        result = contact_list.iterator()
                        name_list = []
                        for n in result:
                            for rec in n:
                                name_list.append(rec.name.value)
                        if name in name_list:
                            print (f"'{name}' is used. Choose another name")
                            continue
                        else:    
                            phone = input("Enter phone (+380XXXXXXXXX or 0XXXXXXXXX):> \n").split()[0]
                            answer = input("Do you need add adress (Y/N):> ").lower()
                            if answer == "y":
                                adress = str(input("Enter adress:> \n"))
                            elif answer == "n":
                                adress = None
                            
                            else:
                                print("Incorrect answer.")
                                continue
                            answer = (input("Do you need add email (Y/N):> ")).lower()
                            if answer == "y":
                                email = input("Enter email:> \n")
                            elif answer == "n":
                                email = None
                            else:
                                print("Incorrect answer.")
                                continue                            
                            answer = (input("Do you need add day of birthday (Y/N):> \n")).lower()
                            if answer == "y":
                                birthday = input("Enter birthday 'YYYY-MM-DD':> \n")
                            elif answer == "n":
                                birthday = None
                            else:
                                print("Incorrect answer.")  
                            print(com_add(contact_book.Name(name), contact_book.Phone(phone), email, adress, birthday))
                            serialized_lpist = contact_list.save_dumped_data()
                        break

                if command == "change number":  #CHANGE NUMBER
                    name = input("Enter name:> ").strip()
                    phone = input("Enter old number:> ").strip()
                    new_phone = input("Enter old number:> ").strip()                   
                    com_change(name, phone , contact_book.Phone(new_phone) )
                    serialized_lpist = contact_list.save_dumped_data()
                

                if command == "show": #show
                    print("Choosing the contact to show...")
                    name = input("Enter name:> ").split()[0]
                    print(com_search(name))


                if command == "delete contact": #delete contact
                    print("Choosing the contact to delete...")
                    name = input("Enter name:> ").strip()
                    com_delete_contact(name)
                    print(f'The contact "{name}" has been delete".\n')


                if command == "add number": #ADD NUMBER
                    name = input("Enter name:> ").split()[0]
                    phone = input("Enter number:> ").split()[0]                    
                    com_join(name,contact_book.Phone(phone))
                    serialized_lpist = contact_list.save_dumped_data()


                if command == "new email": #new EMAIL
                    
                    name = input("Enter name:> ").strip()
                    email = input("Enter email:> ").strip()                  
                    com_join_attribute(name, email = contact_book.Email(email).value)
                    serialized_lpist = contact_list.save_dumped_data()


                if command == "new adress": #new ADRESS

                    name = input("Enter name:> ").strip()
                    adress = input("Enter adress:> ").strip()                    
                    com_join_attribute(name,adress = contact_book.Adress(adress).value)
                    serialized_lpist = contact_list.save_dumped_data()


                if command == "new birthday": #new BIRTHDAY

                    name = input("Enter name:> ").strip()
                    birthday = input("Enter birthday:> ").strip()                  
                    com_join_attribute(name,birthday = contact_book.Birthday(adress).value)
                    serialized_lpist = contact_list.save_dumped_data()


                if command == "delete email": #delete EMAIL
                    
                    name = input("Enter name:> ").strip()
                    email = 'None'                 
                    com_delete_attribute(name,email = email)
                    serialized_lpist = contact_list.save_dumped_data()


                if command == "delete adress": #delete ADRESS

                    name = input("Enter name:> ").strip()
                    adress = 'None'              
                    com_delete_attribute(name,adress = adress)
                    serialized_lpist = contact_list.save_dumped_data()


                if command == "delete birthday": #delete BIRTHDAY

                    name = input("Enter name:> ").strip()
                    birthday = 'None'                
                    com_delete_attribute(name,birthday = birthday)
                    serialized_lpist = contact_list.save_dumped_data()


                if command == "delete number": #DELETE PHONE
                    name = input("Enter name:> ").strip()
                    phone = input("Enter number:> ").strip()                   
                    com_delete(name, phone)
                    serialized_lpist = contact_list.save_dumped_data()
                            


                if command == "show all": # show all
                    result = contact_list.iterator()
                    for n in result:
                        for rec in n:
                            print(f'name: {rec.name.value}; phone: {", ".join([phone.value for phone in rec.phones])};'
                          f' email {rec.email if rec.email else "-"} '  
                          f'adress {rec.adress if rec.adress else "-"} '
                          f'birthday {rec.birthday.value if rec.birthday else "-"} '  
                          )


                if command == "return":
                    print("Return to main menu")
                    with open("experience.dat", "wb") as f:
                        pickle.dump(prediction_experience, f)
                    break

        if command == 'noter': #NOTER
            print ('Noter assistant')
            ######## for HELP 3 NOTER
            commands = ["add note", "show text", "show tag", 
            "delete", "show", "edit", "return", 
            "add tag", "show all",  "sort tag", "find text"]
            
            prediction_experience = {}
            try:
                with open("experience.dat", "rb") as f:
                    prediction_experience = pickle.load(f)
            except FileNotFoundError:
                prediction_experience = {}    
            while True: #NOTER COMAND
                command = str(input("Enter command (add note, delete, show, show all, find, return):>> ")).lower()
                if not command in commands:
                    answer = ""
                    while answer != "y":
                        if command in commands:
                            break
                        for key, value in prediction_experience.items():
                            if command in key:
                                print(f"(d)Perhaps you mean {prediction_experience[key]}")
                                answer = str(input("Answer (Y/N): ")).lower()
                                if answer == "n":
                                    command = str(input("Command input error, try again: ")).lower()
                                elif answer == "y":
                                    command = prediction_experience[key]
                                    break
                        if not command in commands:
                            result = str(difflib.get_close_matches(command, commands, cutoff=0.1, n=1))[2:-2]
                            print(f"Perhaps you mean {result}")
                            answer = str(input("Answer (Y/N): ")).lower()
                            if answer == "n":
                                command = str(input("Command input error, try again: ")).lower()
                            elif answer == "y":
                                prediction_experience[command] = result
                                command = result
                
                if command == "add note": # ADD NOTE
                    print("Creating a note...")
                    while True:
                        name = str(input("Enter name:> "))
                        if f"{name}.json" in noter.scan():
                            print (f"'{name}' is used. Choose another name")
                            continue
                        else:
                            text = str(input("Enter text:> "))
                            answer = str(input("Do you need tags recording now (Y/N):> ")).lower()
                            if answer == "y":
                                tags = str(input("Enter tags:> "))
                                print(noter.add(name, text, tags))
                            elif answer == "n":
                                print(noter.add(name, text))
                            else:
                                print("Incorrect answer. Default mode is a new note without tag")
                                print(noter.add(name, text))
                        break
                if command == "show": #SHOW
                    print("Choosing the note to show...")
                    name = str(input("Enter name:> "))
                    print(noter.show_note(name))
                if command == "delete": # DELETE
                    print("Choosing the note to delete...")
                    name = str(input("Enter name:> "))
                    print(noter.delete(name))
                if command == "show all": # SHOW ALL
                    print(noter.scan())
                if command == "return": # return
                    print("Return to main menu")
                    with open("experience.dat", "wb") as f:
                        pickle.dump(prediction_experience, f)
                    break

        if command == 'sort file': #SORT FILE
            ############ HELP 4 
            user_input = input(
                'Enter the directory for sorting (disk:/folder/folder/) ').split()
            sort_file.start(user_input)

        if command == 'exit':
            
            break

