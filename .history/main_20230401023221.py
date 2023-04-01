from collections import contactDict
from functools import wraps
import re


class Field:
   def __init__(self, value):
       self.value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        if self.value.isnumeric() or len(self.value) < 3: #name validation during init
            self.value = None
            raise ValueError
    
        
class Phone(Field):
    min_len = 5
    max_len = 17
    def __init__(self, value):
            super().__init__(value)
            new_phone = (                  #phone validation during init
                self.value.strip()
                .removeprefix("+")
                .replace("(", "")
                .replace(")", "")
                .replace("-", "")
            )
            if not new_phone.isdecimal() or not Phone.min_len <= len(phone) <= Phone.max_len:
                self.value = None
                raise ValueError
            self.value = new_phone


class Record:
    phones = []
    def __init__(self, name:Name, phone:Phone=None):
        self.name = name
        if phone:
           self.phones.append(phone) 
    
    def add_phone(self, phone:Phone):
        self.phones.append(phone) 
    
    def show_phones(self):
        if len(self.phones) == 0:
            return ('this contact has no phones.')
        elif len(self.phones) == 1:
            return (f'Current phone number is {self.phones[0].value}')
        else:
            output = "This contact has several phones:\n"
            for i, phone in enumerate(self.phones,1):
                output += (f'{i}: {phone.value} ')
            return output
            
    def del_phone(self, num=1):    
        if len(self.phones) == 0:
            raise IndexError
        else:
            self.phones.pop(num-1)
       
    def edit_phone(self, phone_new:Phone, num=1):    
        if len(self.phones) == 0:
            raise IndexError
        else:
            self.phones.insert(num, phone_new)  
         

class AddressBook(contactDict):
    
    def add_record(self,record:Record):
        self.data.update({record.name.value:record})
        
    def remove_record(self, name:str):
        self.data.pop(name)
        
    def show_phone(self, name:str):
        return self.data.get(name).show_phones()
        
    def show_all(self):
        output = ""
        for contact in self.data.keys():
            output += f"{contact}\n" 
            output += "\n".join([phone.value for phone in self.data.get(contact).phones])
        return output
    

    
    
contacts = {}

book1 = AddressBook()


def input_error(func):
    
    @wraps(func)
    def wrapper(*args):

        try:
            result = func(*args)
            return result
       
        except TypeError:
            if func.__name__ == 'handler':
               return 'No such command!'
            if func.__name__ == 'add' or func.__name__ == 'change':
               return f'Give me name and phone please. Minimum phone number length is {Phone.min_len} digits. Maximum {Phone.max_len}. Letters not allowed!'
        
        except KeyError:
            if func.__name__ == 'change' or func.__name__ == 'phone':
               return 'No such contact! to add one use "add" command' 
        
        except ValueError:
            if func.__name__ == 'add' or func.__name__ == 'change':
               return 'Name cannot consist of only digits.'
            if func.__name__ == 'phone':
               return 'Enter contact name' 
            if func.__name__ == 'show_all':
               return 'The Phonebook is empty' 
        
        except IndexError:
                return 'Command needs no arguments'
    
    return wrapper


 
@input_error  
def greet(*args):
    if args != ('',):
        raise IndexError
    return 'How can I help you?'

    
@input_error  
def add(contact:str, phone:str = None):    # в клас AddressBook
    contact_new = Name(contact)
    phone_new = Phone(phone)
    rec_new = Record(contact_new, phone_new)
    book1.add_record(rec_new)
    return f'Added contact "{contact}" with phone number: {phone}'
 
    
@input_error      
def change(contact:str, phone:str = None):   # в клас рекорд
            
    if contact not in book1.keys():
        raise KeyError
    
    if not phone or len(book1.get(contact).phones) > 1: 
       book1.show_phones(contact)
       num = int(input("which one do yo want to change (enter index):"))
       

    else:
        book1.show_phones(contact)
        phone_new = Phone(phone)
        book1.get(contact).edit_phone(phone_new)
        return f'Changed phone number to {phone} for contact "{contact}"'


def del_phone(contact:str):
    book1.get(contact).show_phones()
    if len(record.phones) == 1:
        ans = None
        while ans != 'n' or ans != 'y':
            ans = input(f"Contact {self.name.value} has only 1 phone {self.phones.value}. Are you sure? (Y/N)").lower()    
        if ans == 'y':
            book1.get(contact).del_phone()
    else:     
        
  
   
@input_error      
def phone(contact: str):     
    return f'contact "{contact}" has the following phone number: {book1.show_phone(contact)}' #в клас адресбук


@input_error  
def show_all(*args):
    if args != ('',):
        raise IndexError
    return book1.show_all()

   

COMMANDS = {'hello':greet, 'add':add, 'change':change, 'phone': phone, 
            'show all': show_all}

def command_parser(line: str): 
    
    line_prep = " ".join(line.split())
    for k, v in COMMANDS.items():
        if line_prep.lower().startswith(k+" ") or line_prep.lower() == k: 
            return v, re.sub(k, '', line_prep, flags=re.IGNORECASE).strip().rsplit(' ',1)
    return None, []


@input_error
def handler(command, args):
        return command(*args)


def main():

    while True:
        s = input(">>>")
        if s == 'good bye' or 'close' or 'exit':
            print('Good bye!')
            break
        command, args = command_parser(s)
        print(handler(command, args))
        

if __name__ == '__main__':
    main()