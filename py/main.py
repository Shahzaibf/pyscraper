import PySimpleGUI as sg
from submit import *

# All the stuff inside your window.
layout = [[sg.Text(text="Insert your link:", justification='center', size=(40, 1))],
          [sg.InputText(key='-INPUT-')],
          [sg.Button('Submit'), sg.Button('Cancel')],
          [sg.Multiline(key='-OUT-', disabled=True, size=(60, 15))]
          ]

# Create the Window
window = sg.Window(
    'PyScraper',
    layout,
    size=(500, 500),
    element_justification='center',
    finalize=True
)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    if event == 'Submit':
        if urlChecker(values['-INPUT-']):
            raw = onSubmit(values['-INPUT-'])
            formatted = raw.replace('<', '\n<')
            window['-OUT-'].update(formatted)
        else:
            sg.popup('Not a valid link!', title="Error",
                     font=("Arial Bold", 16))

window.close()
