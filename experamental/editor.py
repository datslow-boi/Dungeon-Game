import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog

from helper import *

class Editor:
    def __init__(self) -> None:
        self.root = tk.Tk()

        self.image_file = ""
        self.items_file = load_json("data\items.json")
        #print(self.items_file)

        #self.root.geometry("800x500")
        self.root.title("Dungeon Builder")

        self.item_frame = tk.Frame(self.root)
        self.item_frame.pack()

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.select_image_button = tk.Button(self.item_frame, text="Select Image", font=("Arial", 18), command=self.open_image)
        self.select_image_button.grid(row=0, column=1)

        self.label = tk.Label(self.item_frame, text="Items", font=("Arial", 18))
        self.label.grid(row=1)

        options = ["equipment", "consume"]
        self.default = tk.StringVar()
        self.default.set( "equipment" )

        self.drop = tk.OptionMenu(self.item_frame, self.default, *options, command=lambda option: self.show_type(self.default))
        self.drop.grid(row=2)

        


        self.root.mainloop()

    def show_type(self, option):
        print(f"Selected option: {option.get()}")

        for widget in self.frame.winfo_children():
            widget.destroy()

        if option.get() == "equipment":
            self.equipment()
        elif option.get() == "consume":
            self.consume()

    def equipment(self):
        self.label = tk.Label(self.frame, text="equipment", font=("Arial", 18))
        self.label.grid(row=0, column=0)

        # Name
        self.name_var = tk.StringVar()
        self.label = tk.Label(self.frame, text="Name", font=("Arial", 12))
        self.label.grid(row=1, column=0)
        self.name_field = tk.Entry(self.frame, textvariable=self.name_var)
        self.name_field.grid(row=2, column=0)

        # Atk
        self.atk_var = tk.StringVar()
        self.atk_label = tk.Label(self.frame, text="Atk", font=("Arial", 12))
        self.atk_label.grid(row=3, column=0)
        self.atk_field = tk.Entry(self.frame, textvariable=self.atk_var)
        self.atk_field.grid(row=4, column=0)

        # Deff
        self.deff_var = tk.StringVar()
        self.deff_label = tk.Label(self.frame, text="Deff", font=("Arial", 12))
        self.deff_label.grid(row=5, column=0)
        self.deff_field = tk.Entry(self.frame, textvariable=self.deff_var)
        self.deff_field.grid(row=6, column=0)

        # Slots
        self.slots_label = tk.Label(self.frame, text="Slots", font=("Arial", 12))
        self.slots_label.grid(row=7, column=0)
        
        self.chest_state = tk.IntVar()
        self.chest_box = tk.Checkbutton(self.frame, text="Chest", font=("Arial", 12), variable=self.chest_state)
        self.chest_box.grid(row=8, column=0)
        
        self.legs_state = tk.IntVar()
        self.legs_box = tk.Checkbutton(self.frame, text="Legs", font=("Arial", 12), variable=self.legs_state)
        self.legs_box.grid(row=8, column=1)
        
        self.head_state = tk.IntVar()
        self.head_box = tk.Checkbutton(self.frame, text="Head", font=("Arial", 12), variable=self.head_state)
        self.head_box.grid(row=9, column=0)
        
        self.weapon_state = tk.IntVar()
        self.weapon_box = tk.Checkbutton(self.frame, text="Weapon", font=("Arial", 12), variable=self.weapon_state)
        self.weapon_box.grid(row=9, column=1)

        # Save button
        self.save_button = tk.Button(self.frame, text="Save", font=("Arial", 18), command=self.save_equipment)
        self.save_button.grid(row=10, column=0)
        

    def consume(self):
        self.label = tk.Label(self.frame, text="consume", font=("Arial", 18))
        self.label.pack(padx=10, pady=10)

    def open_file(self):
        filename = filedialog.askopenfilename(title='open')
        return filename

    def open_image(self):
        self.image_file = self.open_file()
        image = Image.open(self.image_file)
        image.resize(size=(100, 100))
        image = ImageTk.PhotoImage(image)
        panel = tk.Label(self.item_frame, image=image)
        panel.image = image
        panel.grid(row=0, column=0)

    def save_equipment(self):
        temp_dict = {}
        key = list(self.items_file)[-1]
        uid = str(int(key)+1)
        temp_dict[uid] = {}

        state_test = self.chest_state.get() + self.legs_state.get() + self.head_state.get() + self.weapon_state.get()
        if state_test == 0:
            messagebox.showerror(message="You have to select a slot!")
            return
        if state_test > 1:
            messagebox.showerror(message="You can't select more then one slot")
            return
        
        try:
            self.atk_var =  int(self.atk_var.get())
            self.deff_var = int(self.deff_var.get())
        except:
            messagebox.showerror(message="atk and def have to be ints")
            return

        temp_dict[uid]["type"] = "equipment"
        temp_dict[uid]["path"] = self.image_file
        temp_dict[uid]["name"] = self.name_var.get()

        if self.atk_var > 0:
            temp_dict[uid]["atk"] = self.atk_var
        if self.deff_var > 0:
            temp_dict[uid]["deff"] = self.deff_var

        if bool(self.chest_state.get()):
            print("chest")
            temp_dict[uid]["chest"] = True
        elif bool(self.legs_state.get()):
            print("legs")
            temp_dict[uid]["legs"] = True
        elif bool(self.head_state.get()):
            print("Head")
            temp_dict[uid]["head"] = True
        elif bool(self.weapon_state.get()):
            print("weapon")
            temp_dict[uid]["weapon"] = True

        
        print(temp_dict)

if __name__ == "__main__":
    editor = Editor()

