from pynput import keyboard


def execute(combo):
    controller = keyboard.Controller()
    for _ in combo:
        controller.press(keyboard.Key.backspace)
        controller.release(keyboard.Key.backspace)
    controller.type(combos[combo])


def on_press(key):
    global current, listining
    try:
        if any([combo for combo in combos if combo.startswith(key.char)]):
            print("begining detected")
            listining = True
        if listining:
            current += key.char
            print(current)
            print(listining)
            if current in combos:
                execute(current)
                listining = False
                current = ""
            elif len(current) > max_combo:
                listining = False
                current = ""

    except AttributeError:
        pass


def on_release(key):
    pass


combos = {
    ";ha": "Hassanien",
    ";ak": "Alkaissi",
    ";hk": "Hassanien Alkaissi",
}
max_combo = len(max(combos, key=lambda s: len(s)))
current = ""

listining = False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()