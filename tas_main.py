import time, keyboard, vgamepad as vg
from tas_io_handler import tas_io as io

btn = vg.XUSB_BUTTON
con = vg.VX360Gamepad()

def press(con:vg.VX360Gamepad, btns:list[btn], presses:int=1, delay:int=0):
    for _ in range(presses):
        con.press_button(*btns)
        con.update()
        time.sleep(1/60)
        con.release_button(*btns)
        con.update()
        if delay>0:
            time.sleep(1/60)

class tas_main(io):
    def __init__(self, file='.tas'):
        self.file = file
        self.inputs = []
        self.presses = []  

    def init(self):
        self.inputs = self.load()
    
    def update_presses(self, key:keyboard.KeyboardEvent):
        if key.event_type == 'down':
            if not key.scan_code in self.presses:
                self.presses.append(key.scan_code)
        else:
            if key.scan_code in self.presses:
                self.presses.remove(key.scan_code)
    
    def update_inputs(self, *b):
        decode,a = {72:'u',
                    80:'d',
                    75:'l',
                    77:'r',
                    16:'a',
                    48:'b',
                    21:'y',
                    31:'s'},''
        if self.presses == []:
            a = 'n'
        else:
            for i in self.presses:
                a += decode[i]
        tas.inputs.append(a)

    def record(self, overwrite:int=0):
        print('Started recording...')
        print('Press Enter to stop recording.')
        if overwrite>0:
            tas.inputs = []
            print('Warning: You are overwriting the currently loaded inputs.')
        keyboard.hook_key(key='up', callback=self.update_presses)
        keyboard.hook_key(key='down', callback=self.update_presses)
        keyboard.hook_key(key='left', callback=self.update_presses)
        keyboard.hook_key(key='right', callback=self.update_presses)
        keyboard.hook_key(key='a', callback=self.update_presses)
        keyboard.hook_key(key='b', callback=self.update_presses)
        keyboard.hook_key(key='y', callback=self.update_presses)
        keyboard.hook_key(key='s', callback=self.update_presses)
        keyboard.hook_key(key='enter', callback=self.update_presses)
        keyboard.on_press_key(key='f', callback=self.update_inputs)
        while 28 not in self.presses:
            time.sleep(1/60) # i don't need to busy wait since timing precision isn't as important here
        keyboard.unhook_all_hotkeys()
        print('Stopped recording.')

    def run(self, length:int=-1, pause:int=0):
        print('Running TAS in 3 seconds...')
        print('Warning: Make sure the game is running and the window is focused.')
        time.sleep(2)
        press(con, [btn.XUSB_GAMEPAD_A])
        time.sleep(1)
        press(con, [btn.XUSB_GAMEPAD_START])
        press(con, [btn.XUSB_GAMEPAD_RIGHT_SHOULDER])
        d = 18/60+time.perf_counter()
        while time.perf_counter()<d:
            pass
        s_t = time.perf_counter()
        s = time.perf_counter()
        for i in enumerate(self.inputs):
            if i[0] == length-1:
                break
            con.reset()
            con.update()
            x,y=0,0
            for j in i[1]:
                match j:
                    case 'u':
                        y=32767
                    case 'd':
                        y=-32768
                    case 'l':
                        x=-32768
                    case 'r':
                        x=32767
                    case 'a':
                        con.press_button(btn.XUSB_GAMEPAD_B)
                    case 'b':
                        con.press_button(btn.XUSB_GAMEPAD_Y)
                    case 'y':
                        con.press_button(btn.XUSB_GAMEPAD_A)
                    case 's':
                        con.left_trigger(255)
                    case 'n':
                        x,y=0,0
                        con.reset()
                    case _:
                        raise ValueError(f"Invalid input: {j}")
            con.left_joystick(x,y)
            con.update()
            d = 1/60+s
            while time.perf_counter()<d:
                pass # i'm busy waiting in order to maintain high timing precision to avoid desynchronizing with the game
            s = time.perf_counter()
        d_t = time.perf_counter()
        if pause:
            press(con, btn.XUSB_GAMEPAD_START)
        con.reset()
        con.update()
        print('')
        print(f'frame count: {len(self.inputs)}')
        print('')
        print(f'theoratical total time: {len(self.inputs)/60}')
        print(f'total measured time: {d_t-s_t}')
        print(f'difference: {abs((d_t-s_t)-(len(self.inputs)/60))}')
        print('')
        print(f'theoratical frame length: {1/60}')
        print(f'average frame length: {(d_t-s_t)/len(self.inputs)}')
        print(f'difference: {abs(((d_t-s_t)/len(self.inputs))-1/60)}')
        print('')

    def run_debug(self, length:int=-1):
        print('Running TAS in 3 seconds...')
        print('Make sure the game is running and the window is focused.')
        time.sleep(2)
        press(con, [btn.XUSB_GAMEPAD_A])
        time.sleep(1)
        press(con, [btn.XUSB_GAMEPAD_START])
        press(con, [btn.XUSB_GAMEPAD_RIGHT_SHOULDER])
        con.left_trigger(255)
        con.right_trigger(255)
        con.press_button(btn.XUSB_GAMEPAD_DPAD_DOWN)
        con.update()
        time.sleep(1/60)
        con.left_trigger(0)
        con.right_trigger(0)
        con.release_button(btn.XUSB_GAMEPAD_DPAD_DOWN)
        con.update()
        time.sleep(1/60)
        press(con, [btn.XUSB_GAMEPAD_START])
        press(con, [btn.XUSB_GAMEPAD_RIGHT_SHOULDER], 15, 1)
        for i in enumerate(self.inputs):
            if i[0] == length-1:
                break
            con.reset()
            con.update()
            x,y=0,0
            for j in i[1]:
                match j:
                    case 'u':
                        y=32767
                    case 'd':
                        y=-32768
                    case 'l':
                        x=-32768
                    case 'r':
                        x=32767
                    case 'a':
                        con.press_button(btn.XUSB_GAMEPAD_B)
                    case 'b':
                        con.press_button(btn.XUSB_GAMEPAD_Y)
                    case 'y':
                        con.press_button(btn.XUSB_GAMEPAD_A)
                    case 's':
                        con.left_trigger(255)
                    case 'n':
                        x,y=0,0
                        con.reset()
                    case _:
                        raise ValueError(f"Invalid input: {j}")
            con.left_joystick(x,y)
            con.press_button(btn.XUSB_GAMEPAD_RIGHT_SHOULDER)
            con.update()
            time.sleep(1/60)
            con.release_button(btn.XUSB_GAMEPAD_RIGHT_SHOULDER)
            con.update()
            time.sleep(1/60)
        con.reset()
        con.update()

a = input('file name: ')
tas = tas_main(a)
try:
    tas.init()
except FileNotFoundError:
    print('File not found, you will have to save inputs first to create a new .tas file.')

while True:
    a = input('command: ').split()

    try:
        match a[0]:
            case 'run':
                try:
                    tas.run(int(a[1]), int(a[2]))
                except IndexError:
                    tas.run()
            case 'save':
                tas.save(tas.inputs)
            case 'load':
                tas.file = a[1]
                tas.init()
            case 'load_inputs':
                tas.inputs = a[1].split(';')
            case 'add':
                tas.inputs.append(a[1])
            case 'insert':
                tas.inputs.insert(int(a[1])-1, a[2])
            case 'replace':
                tas.inputs[int(a[1])-1] = a[2]
            case 'delete':
                tas.inputs.pop(int(a[1])-1)
            case 'run_debug':
                try:
                    tas.run_debug(int(a[1]))
                except IndexError:
                    tas.run_debug()
            case 'print':
                print(';'.join(tas.inputs))
            case 'record':
                try:
                    tas.record(int(a[1]))
                except:
                    tas.record()
            case 'exit':
                break
            case _:
                print('Invalid command.')
    except:
        print('Invalid command.')