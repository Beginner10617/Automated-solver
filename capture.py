'''
    Protocol for capturing:
    1. Take the cursor to the top-left corner
    2. Left click to track it, you can do this multiple times
    3. After deciding the corner, capture it by right-click
    4. Do the same to capture bottom-right corner
'''

from pynput import mouse
import mss
import mss.tools

Corners = []   # Corner extremes
x, y = 0, 0 # Current Input
captureMode = 1 # Capturing first corner

def capture_corner():
    global captureMode
    if captureMode > 2: return False
    Corners.append((x, y))
    captureMode += 1
    return captureMode <= 2

def track_cursor(a, b):
    global x, y
    x, y = a, b
    return True

def on_click(x, y, button, pressed):
    if(not pressed): return True
    if button == mouse.Button.left:
        return track_cursor(x, y)
    elif button == mouse.Button.right:
        return capture_corner()

def capture_protocol():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

def take_screenshot(x1, y1, x2, y2, filename="screenshot.png"):
    region = {
    "left": x1,
    "top": y1,
    "width": x2 - x1,
    "height": y2 - y1
}

    with mss.mss() as sct:
        cropped = sct.grab(region)
        mss.tools.to_png(cropped.rgb, cropped.size, output=filename)

def main(filename='main.png', firstIter = True):
    print("CAPTURE THE DESIRED REGION ON THE SCREEN")
    if firstIter: capture_protocol()
    take_screenshot(Corners[0][0], Corners[0][1], Corners[1][0], Corners[1][1], filename)
    return filename

if __name__ == '__main__':
    main()