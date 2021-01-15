import os
import tkinter as tk
from tkinter.messagebox import showinfo


def popup_showinfo():
    Detalii = 'Aici ar trebui sa fie interfata unui server mqtt!'
    showinfo("Detalii", Detalii)

class Parser:
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    A = None
    B = None

    def __init__(self, gui):
        self.gui = gui
        self.gui.title('SERVER MQTT')

        self.gui.geometry("600x600")
        nume = tk.Label(gui, text='SERVER MQTT', background="lightcyan", font=('Helvetica', 14, 'bold'),
                     width=40, height=3)
        nume.place(x=100, y=10)

        btnChange = tk.Button(gui, text="Start", font=('Helvetica', 10, 'bold'), width=10, height=2,
                               background="mistyrose"
                              )

        btnChange2 = tk.Button(gui, text="Stop", font=('Helvetica', 10, 'bold'), width=10, height=2,
                            background="mistyrose")
        btnChange.place(x=200, y=500)
        btnChange2.place(x=300, y=500)

        button3 = tk.Button(gui, text="Detalii", font=('Helvetica', 10, 'bold'), background="mistyrose", height=2,
                         width=10, command=popup_showinfo)
        button3.pack()
        button3.place(x=400, y=500)
        result_text = tk.Text(gui, width=60, height=23)
        result_text.place(x=100, y=110)
        result_text.insert(tk.END, 'Aici se vor afisa pachetele trimise: ')





        self.gui.mainloop()






if __name__ == '__main__':
    root = tk.Tk()
    root.title('Server MQTT')
    app = Parser(root)
    root.mainloop()
