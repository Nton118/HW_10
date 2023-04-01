from collections import UserDict
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
    
        
class Phone(Field):
    min_len = 5
    max_len = 17
    def __init__(self, value):
            super().__init__(value)
            new_phone = (
                phone.strip()
                .removeprefix("+")
                .replace("(", "")
                .replace(")", "")
                .replace("-", "")
            )
            if not new_phone.isdecimal() or not Phone.min_len <= len(phone) <= Phone.max_len:
                self.value = None
            self.value = new_phone


class Record:
    phones = []
    def __init__(self, name:Name, phone:Phone=None):
        self.name.value = name
        if phone:
           self.phones.append(Phone.value) 
    
    def add_phone(self, Phone):
        self.phones.append(Phone.value) 
        
    def del_phone(self):    
        if len(self.phones) == 0:
            print('this contact has no phones!')
        if len(self.phones) == 1:
            ans = None
            while ans != 'n' or ans != 'y':
                ans = input("Contact {self.name.value} has only 1 phone {self.phone.value}. Are you sure? (Y/N)").lower()    
            if ans == 'y':
                self.phones.clear()
        if len(self.phones) > 1:
            print('this contact has several phones:')
            for i, phone in enumerate(self.phones,1):
                print(f'{i}: {phone}')
            num = input('Which one do you want to delete?')

    
    
    def edit_phone(self)    
        
class AddressBook(UserDict):
    def add_record(self,Record):
        self.data = {Record.name.value:Record.phones}
        
    def remove_record()


users = {}

is_ended = False


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
               return 'No such user! to add one use "add" command' 
        
        except ValueError:
            if func.__name__ == 'add' or func.__name__ == 'change':
               return 'Name cannot consist of only digits.'
            if func.__name__ == 'phone':
               return 'Enter user name' 
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
def add(user: str, phone: str):    # в клас AddressBook
    
    phone_corr = sanitize_phone_number(phone)
    if not user or not phone_corr:
        raise TypeError
   
    if  user.isdigit(): # в клас нейм
        raise ValueError 
    
    users[user] = phone_corr
    return f'Added user "{user}" with phone number: {phone}'
 
    
@input_error      
def change(user: str, phone: str):   # в клас рекорд
    
    phone_corr = sanitize_phone_number(phone)
    if not user or not phone_corr:
        raise TypeError
    
    if user not in users.keys():
        raise KeyError
    
    phone_corr = sanitize_phone_number(phone)
    
    users[user] = phone_corr
    return f'Changed phone number to {phone} for user "{user}"'
  
   
@input_error      
def phone(user: str): 
    
    if not user:
        raise ValueError
    
    if user not in users.keys():
        raise KeyError    
    
    return f'user "{user}" has the following phone number: {users.get(user)}' #в клас адресбук


@input_error  
def show_all(*args):
    
    if args != ('',):
        raise IndexError
    
    if len(users) == 0: #в клас адресбук
        raise ValueError
    
    output = ""
    for user in users.keys():
        output += f"{user}: {users.get(user)}\n" #в клас адресбук
    
    return output


@input_error  
def exit(*args):
    if args != ('',):
        raise IndexError
    global is_ended
    is_ended = True
    return ('Good bye!')
    

COMMANDS = {'hello':greet, 'add':add, 'change':change, 'phone': phone, 
            'show all': show_all, 'good bye': exit, 'close': exit, 'exit': exit}


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
    while not is_ended:
        s = input(">>>")
        command, args = command_parser(s)
        print(handler(command, args))
        

if __name__ == '__main__':
    main()