from collections import UserDict
from functools import wraps
import re

SHORTEST_PHONE_NUM_LEN = 5
LONGEST_PHONE_NUM_LEN = 17

class Field:
   def __init__(self, value):
       self.value = value

class Name(Field):
    def __init__(self, value):
       super().__init__
       
        
class Phone(Field):
    pass

class Record:
    pass

class AddressBook(UserDict):
    pass



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
               return f'Give me name and phone please. Minimum phone number length is {SHORTEST_PHONE_NUM_LEN} digits. Maximum {LONGEST_PHONE_NUM_LEN}. Letters not allowed!'
        
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

def sanitize_phone_number(phone):
         
    new_phone = (
        phone.strip()
        .removeprefix("+")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
    )
    if not new_phone.isdecimal() or not SHORTEST_PHONE_NUM_LEN <= len(phone) <= LONGEST_PHONE_NUM_LEN:
        return None
    return new_phone
 
@input_error  
def greet(*args):
    
    if args != ('',):
        raise IndexError
    
    return 'How can I help you?'

    
@input_error  
def add(user: str, phone: str):    
    
    phone_corr = sanitize_phone_number(phone)
    if not user or not phone_corr:
        raise TypeError
   
    if  user.isdigit():
        raise ValueError 
    
    users[user] = phone_corr
    return f'Added user "{user}" with phone number: {phone}'
 
    
@input_error      
def change(user: str, phone: str):
    
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
    
    return f'user "{user}" has the following phone number: {users.get(user)}'


@input_error  
def show_all(*args):
    
    if args != ('',):
        raise IndexError
    
    if len(users) == 0:
        raise ValueError
    
    output = ""
    for user in users.keys():
        output += f"{user}: {users.get(user)}\n"
    
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