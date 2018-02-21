import demoscope3
from tkinter import *

master = Tk()

def buttonfunction(index):
	for i in range(3):
		buttons[i].config(state="disabled")
	if index == 0:
		demoscope3.scope()
	elif index == 1:
		demoscope3.storedata()
	elif index == 2:
		exit()
	for i in range(3):
		buttons[i].config(state="active")
	

button_names = ['Plotear en tiempo real', 'Adquirir y almacenar', 'Salir']

buttons = []

for index in range(3): 
    n=button_names[index]

    button = Button(master, bg="White", text=n, relief=GROOVE,
                    command=lambda index=index, n=n: buttonfunction(index))

    # Add the button to the window
    button.grid(padx=2, pady=2, row=index%3, column=0)

    # Add a reference to the button to 'buttons'
    buttons.append(button)

mainloop()
