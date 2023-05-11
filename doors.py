from abc import ABC, abstractmethod
import time

class Door():
    def __init__(self, id, code_handler):
        self.id = id
        self._code_handler = code_handler
        self.num_trials = 0
        self.locked = False
        self.MAX_TRIALS = 3
        
    def process_code(self, code):
        self._code_handler.handle_code(code, self)
    def open(self):
        print('\topen door {}'.format(self.id))
        
    def reset_state(self):
        self.num_trials = 0
        self.locked = False
    
        

class CodeHandler(ABC):
    def __init__(self, next):
        self.next_handler = next
        
    def handle_code(self, code, door):
        if self.next_handler is not None:
            self.next_handler.handle_code(code, door)
    

class Log(CodeHandler):
    def handle_code(self, code, door):
        print("-----handle Log-----")
        is_locked = "is locked, " if door.locked else ""
        print("\tcode {} door {}, {} at {}".format(code, door.id, is_locked, time.asctime()))
        super().handle_code(code, door)

class Open(CodeHandler):
    def __init__(self, code, next_handler):
        self._code = code
        super().__init__(next_handler)
        
    def handle_code(self, code, door):
        next = True
        print("-----handle Open-----")
        if not door.locked:
            if code == self._code:
                print("\tDoor opened")
                door.reset_state()
                door.open()
            else:
                print("\twrong code!")
                door.num_trials +=1
                print("\t{} trials".format(door.num_trials))
                if door.num_trials >= door.MAX_TRIALS:
                    print("\tdoor should be locked")
                    next = False
                    Lock(self.next_handler).handle_code(self._code, door)
                    
        else:
            print("\tdoor locked, unlock to open")
        if next:  
            super().handle_code(code, door)

class FireAlarm(CodeHandler):
    def __init__(self, code, next_handler):
        self._code = code
        super().__init__(next_handler)
        
    def handle_code(self, code, door):
        next = True
        print("-----handle FireAlarm-----")
        if not door.locked:
            if code == self._code:
                print("\tFire Alarm on!")
                print("\tdoor opened")
                door.reset_state()
                door.open()
            else:
                print("\tWrong code")
                door.num_trials +=1
                print("\t{} trials".format(door.num_trials))
                if door.num_trials >= 3:
                    print("\tdoor should be locked")
                    next = False
                    Lock(self.next_handler).handle_code(self._code, door)

        else:
            print("\tdoor locked, unlock activate fire alarm")
        if next:
            super().handle_code(code, door)
        
        
class Unlock(CodeHandler):
    def __init__(self, code, next_handler):
        self._code = code
        super().__init__(next_handler)
        
    def handle_code(self, code, door):
        print("-----handle Unlock-----")
        if door.locked:
            if code == self._code:
                print("\tDoor unlocked")
                door.reset_state()
            else:
                print("\tDoor still locked, wrong code")
        else:
            print("\tDoor already unlocked")
        super().handle_code(code, door)
            
class Lock(CodeHandler):
    def handle_code(self, code, door):
        print("-----handle Lock-----")
        if not door.locked:
            door.locked = True
            print("\tdoor locked")
        else:
            print("\tAlready locked")
        super().handle_code(code, door)
        


if __name__ == '__main__':
    code_open, code_fire_alarm, code_unlock = '1111','2222','3333'
    
    chain1 = Log(Unlock(code_unlock, FireAlarm(code_fire_alarm,
    Open(code_open, Lock(None)))))
    
    chain2 = Log(Open(code_open, None))
    chain3 = Log(FireAlarm(code_fire_alarm, Open(code_open, None)))
    d1 = Door('d1', chain1)
    print("\n######TEST on chain 1######\n")
    print("TRY 1")
    d1.process_code('1111') # opens
    print("TRY 2")
    d1.process_code('2222') # opens and fires alarm
    print("TRY 3")
    d1.process_code('1234') # first trial
    #d1.process_code('1234')
    # ... same as before
    # change behaviour of d1 at execution time
    d1.reset_state()
    d1._code_handler = chain2
    print("\n######TEST on chain 2######\n")
    print("TRY 1")
    d1.process_code('1111') # opens
    print("TRY 2")
    d1.process_code('2222') # opens and fires alarm
    print("TRY 3")
    d1.process_code('1234') # first trial
    
    d1.reset_state()
    d1._code_handler = chain3
    print("\n######TEST on chain 3######\n")
    
    print("TRY 1")
    d1.process_code('1111') # opens
    print("TRY 2")
    d1.process_code('2222') # opens and fires alarm
    print("TRY 3")
    d1.process_code('1234') # first trial