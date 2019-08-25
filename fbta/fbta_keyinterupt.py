from pynput import keyboard


class FBTAKeyInterupt:
    def __init__(self):
        self.__COMBINATION = {keyboard.KeyCode.from_char('c'), keyboard.KeyCode.from_char('x')}
        self.__current = set()
        self.__interrupt = keyboard.Listener(on_press=self.__on_press)

    @property
    def interrupt(self):
        return self.__interrupt

    def start(self):
        self.__interrupt.start()

    def __on_press(self, key):
        if key in self.__COMBINATION:
            self.__current.add(key)
            if all(k in self.__current for k in self.__COMBINATION):
                print('Key Interrupt pressed: ', self.__current)
                raise KeyboardInterrupt('Key Error')
        if key == keyboard.Key.esc:
            self.__interrupt.stop()

    def __on_release(self, key):
        try:
            self.__current.remove(key)
        except KeyError:
            pass
