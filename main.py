import time
import mido
import display

if __name__ == "__main__":
    disp = display.Display()
    with mido.open_input('midi_viewer_in', virtual=True, callback=disp.receive) as inport:
        # Instantiate composer
        # # Install callback function for input
        # inport.callback = disp.receive
        while (disp.running):
            disp.update()
            time.sleep(0.1)