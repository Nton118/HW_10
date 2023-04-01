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
            if (not new_phone.isdecimal() or 
                not Phone.min_len <= len(new_phone) <= Phone.max_len):
                self.value = None
                raise ValueError
            self.value = new_phone


class Record:
    count = 0
    
    def __init__(self, name:Name, phone:Phone=None):
        self.name = name
        self.phones = []
        if phone:
           self.phones.append(phone) 
        Record.count += 1
    
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
            return self.phones.pop(num-1)
       
    def edit_phone(self, phone_new:Phone, num=1):    
        if len(self.phones) == 0:
            raise IndexError
        else:
            self.phones.pop(num-1)
            self.phones.insert(num-1, phone_new)  
            

            

class AddressBook(UserDict):
    
    def add_record(self,record:Record):
        self.data.update({record.name.value:record})
        
        
    def remove_record(self, contact:str):
        return self.data.pop(contact)
        
    def show_phone(self, contact:str):
        return self.data.get(contact).show_phones()
        
    def show_all(self):
        output = ""
        for contact in self.data.keys():
            output += (f"{contact}: {'; '.join([phone.value for phone in self.data.get(contact).phones])}") 
        return output
    
   
    
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
               return f'''Give me name and phone please. Minimum phone number length is 
                       {Phone.min_len} digits. Maximum {Phone.max_len}. 
                       Letters not allowed!'''
        
        except AttributeError:
            if (func.__name__ == 'change' or func.__name__ == 'phone' 
                or func.__name__ == 'del_contact' or func.__name__ == 'del_phone'):
               return 'No such contact! to add one use "add" command' 
        
        except ValueError:
            if func.__name__ == 'add' or func.__name__ == 'change':
               return 'Name cannot consist of only digits and min name length is 3.'
            if func.__name__ == 'phone':
               return 'Enter contact name' 
            if func.__name__ == 'show_all':
               return 'The Phonebook is empty' 
            if func.__name__ == 'del_phone':
               return "this contact doesn't have such phone number!" 
        
        except IndexError:
               return 'Command needs no arguments'
    
    return wrapper

 
@input_error  
def greet(*args):
    if args != ('',):
        raise IndexError
    return 'How can I help you?'

    
@input_error  
def add(contact:str, phone:str = None):
    
    contact_new = Name(contact)
    phone_new = Phone(phone) if phone else None
    rec_new = Record(contact_new, phone_new)
    
    if contact not in book1.keys(): 
        book1.add_record(rec_new)
        return f'Added contact "{contact}" with phone number: {phone}'
    else:
        book1.get(contact).add_phone(phone_new)
        return f'Updated existing contact "{contact}" with new phone number: {phone}'
        
    
@input_error      
def change(contact:str, phone:str = None):    

    rec = book1.get(contact)
    
    print(book1.show_phone(contact))
    
    if len(rec.phones) == 0: 
        if not phone:
            phone_new = Phone(input("If you want to add the phone enter phone number:"))
        else:   
            phone_new = Phone(phone)
        rec.add_phone(phone_new)
        return f'Changed phone number to {phone_new.value} for contact "{contact}"'
    
    else: 
        if len(rec.phones) == 1:
            num = 1
        if len(rec.phones) > 1:   
            num = int(input("which one do yo want to change (enter index):")) 
        if not phone: 
            phone_new = Phone(input("Please enter new phone number:"))
        else:
            phone_new = Phone(phone)     
        old_phone = rec.phones[num-1].value
        rec.edit_phone(phone_new, num)
        return f'''Changed phone number {old_phone} 
                    to {phone_new.value} for contact "{contact}"'''


@input_error  
def del_phone(contact:str, phone=None):
    rec = book1.get(contact)
    
    if not rec:
        raise AttributeError
    
    if phone:
        for i,p in enumerate(rec.phones):
            if p.value == phone:
                num = i+1
        else:
            raise ValueError        
    else:        
        print(rec.show_phones())
        if len(rec.phones) == 1:
            ans = None
            while ans != 'y':
                ans = input(f"Contact {rec.name.value} has only 1 phone {rec.phones[0].value}. Are you sure? (Y/N)").lower()    
        else:     
            num = int(input("which one do yo want to delete (enter index):"))
    return f'Phone {rec.del_phone(num).value} deleted!'
    
@input_error         
def del_contact(contact:str):
    rec = book1.get(contact)
    if not rec:
        raise AttributeError
    ans = None
    while ans != 'y':
        ans = input(f"Are you sure to delete contact {contact}? (Y/N)").lower()
    return f'Contact {book1.remove_record(contact).name.value} deleted!'
   
@input_error      
def phone(contact: str):     
    return f'Contact "{contact}". {book1.show_phone(contact)}' 


@input_error  
def show_all(*args):
    if args != ('',):
        raise IndexError
    return book1.show_all()

@input_error
def help(*args):
    if args != ('',):
        raise IndexError 
    return f"available commands: {', '.join(k for k in COMMANDS.keys())}"  

COMMANDS = {'hello':greet, 'add':add, 'change':change, 'phone': phone, 
            'show all': show_all, 'del phone':del_phone, 'del contact':del_contact, 'help':help}

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
        if s == 'good bye' or s ==  'close' or  s == 'exit':
            print('Good bye!')
            break
        command, args = command_parser(s)
        print(handler(command, args))
        

if __name__ == '__main__':
    main()