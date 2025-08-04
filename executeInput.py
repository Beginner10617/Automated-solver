from pynput import mouse, keyboard

mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()

def executeCmd(x : str) -> None:
    y = list(x.strip().split())
    if len(y) == 0:
        return 
    if y[0] == 'M':
        if y[1] == 'M':
            # Move mouse
            assert len(y) == 4, "Move command requires 2 parameters"
            x_coord = int(y[2])
            y_coord = int(y[3])
            mouse_controller.position = (x_coord, y_coord)
        elif y[1] == 'P':
            # Mouse press
            assert len(y) == 3, "Mouse press command requires 1 parameters"
            button = y[2]
            if button == 'L':
                mouse_controller.press(mouse.Button.left)
            elif button == 'R':
                mouse_controller.press(mouse.Button.right)
            elif button == 'M':
                mouse_controller.press(mouse.Button.middle)
        elif y[1] == 'R':
            # Mouse release
            assert len(y) == 3, "Mouse release command requires 1 parameters"
            button = y[2]
            if button == 'L':
                mouse_controller.release(mouse.Button.left)
            elif button == 'R':
                mouse_controller.release(mouse.Button.right)
            elif button == 'M':
                mouse_controller.release(mouse.Button.middle)
        elif y[1] == 'C':
            # Click = press and release
            assert len(y) == 3, "Click command requires 1 parameters"
            button = y[2]
            if button == 'L':
                mouse_controller.click(mouse.Button.left)
            elif button == 'R':
                mouse_controller.click(mouse.Button.right)
            elif button == 'M':
                mouse_controller.click(mouse.Button.middle)
    elif y[0] == 'K':
        assert len(y) > 1, "Keyboard command requires at least 1 parameters"
        if y[1] == '<SPACE>':
            # Press space
            keyboard_controller.press(keyboard.Key.space)
            keyboard_controller.release(keyboard.Key.space)
        elif y[1] == '<ENTER>':
            # Press enter
            keyboard_controller.press(keyboard.Key.enter)
            keyboard_controller.release(keyboard.Key.enter)
        elif y[1] == '<BACKSPACE>':
            # Press backspace
            keyboard_controller.press(keyboard.Key.backspace)
            keyboard_controller.release(keyboard.Key.backspace)
        elif y[1] == '<ESCAPE>':
            # Press escape
            keyboard_controller.press(keyboard.Key.esc)
            keyboard_controller.release(keyboard.Key.esc)
        elif y[1] == '<LEFT>':
            # Press left arrow
            keyboard_controller.press(keyboard.Key.left)
            keyboard_controller.release(keyboard.Key.left)
        elif y[1] == '<RIGHT>':
            # Press right arrow
            keyboard_controller.press(keyboard.Key.right)
            keyboard_controller.release(keyboard.Key.right)
        elif y[1] == '<UP>':
            # Press up arrow
            keyboard_controller.press(keyboard.Key.up)
            keyboard_controller.release(keyboard.Key.up)
        elif y[1] == '<DOWN>':
            # Press down arrow
            keyboard_controller.press(keyboard.Key.down)
            keyboard_controller.release(keyboard.Key.down)
        else:
            # Press a specific key
            try:
                key = keyboard.KeyCode.from_char(y[1])
                keyboard_controller.press(key)
                keyboard_controller.release(key)
            except ValueError:
                raise ValueError(f"Invalid key: {y[1]}")
    else:
        raise ValueError(f"Unknown command: {y[0]}")
    
def main(filename: str) -> None:
    assert filename, "Filename cannot be empty"
    assert filename.endswith('.txt'), "Filename must end with .txt"
    with open(filename, 'r') as file:
        i = 0
        for line in file:
            try:
                executeCmd(line)
            except Exception as e:
                print(f"Error executing line {i}: {e}")
            i += 1

'''
This script reads commands from a file and executes mouse and keyboard actions based on the commands.
Commands are expected to be in a specific format, such as:
M M 100 200  # Move mouse to (100, 200)
M P L        # Press left mouse button
M R L        # Release left mouse button
M C R        # Click right mouse button
K <SPACE>    # Press space key
K <LEFT>     # Press left arrow key
K <BACKSPACE># Press backspace key
K a          # Press 'a' key
The script uses the pynput library to control mouse and keyboard actions.
'''