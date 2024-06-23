import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("note")
        self.root.geometry("800x600")

        self.config_file = "config.json"
        self.theme = "light"

        # Adding Line Numbers
        self.line_numbers = tk.Text(self.root, width=4, padx=5, takefocus=0, border=0, background='lightgrey', state='disabled')
        self.line_numbers.pack(side='left', fill='y')

        self.text_area = tk.Text(self.root, wrap="word", undo=True)
        self.text_area.pack(side='right', fill="both", expand=True)
        self.text_area.bind('<Any-KeyPress>', self.on_content_changed)
        self.text_area.bind('<Button-1>', self.on_content_changed)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_application, accelerator="Ctrl+Q")

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_area.edit_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.text_area.edit_redo, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=lambda: self.root.focus_get().event_generate("<<Cut>>"), accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=lambda: self.root.focus_get().event_generate("<<Copy>>"), accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=lambda: self.root.focus_get().event_generate("<<Paste>>"), accelerator="Ctrl+V")
        self.edit_menu.add_command(label="Delete", command=lambda: self.text_area.delete("sel.first", "sel.last"), accelerator="Del")
        self.edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")

        self.theme_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Theme", menu=self.theme_menu)
        
        self.light_theme_menu = tk.Menu(self.theme_menu, tearoff=0)
        self.theme_menu.add_cascade(label="Light Themes", menu=self.light_theme_menu)
        self.light_theme_menu.add_command(label="Light Theme", command=self.light_theme)
        self.light_theme_menu.add_command(label="Solarized Light", command=self.solarized_light_theme)

        self.dark_theme_menu = tk.Menu(self.theme_menu, tearoff=0)
        self.theme_menu.add_cascade(label="Dark Themes", menu=self.dark_theme_menu)
        self.dark_theme_menu.add_command(label="Dark Theme", command=self.dark_theme)
        self.dark_theme_menu.add_command(label="Solarized Dark", command=self.solarized_dark_theme)
        self.dark_theme_menu.add_command(label="Monokai", command=self.monokai_theme)
        self.dark_theme_menu.add_command(label="Dracula", command=self.dracula_theme)
        self.dark_theme_menu.add_command(label="Tokyo Night", command=self.tokyo_night_theme)
        self.dark_theme_menu.add_command(label="Gruvbox", command=self.gruvbox_theme)
        self.dark_theme_menu.add_command(label="Nordic", command=self.nordic_theme)  # Add Nordic theme option

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

        self.file_path = None

        self.load_config()

        # Bind shortcuts
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-Shift-S>", lambda event: self.save_as_file())
        self.root.bind("<Control-a>", self.select_all)
        self.root.bind("<Control-q>", lambda event: self.exit_application())  # Bind Ctrl+Q to exit

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.update_line_numbers()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.file_path = file_path
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
            self.update_line_numbers()

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.file_path = file_path
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))

    def select_all(self, event=None):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        return 'break'

    def apply_theme(self):
        if self.theme == "light":
            self.light_theme()
        elif self.theme == "solarized_light":
            self.solarized_light_theme()
        elif self.theme == "dark":
            self.dark_theme()
        elif self.theme == "solarized_dark":
            self.solarized_dark_theme()
        elif self.theme == "monokai":
            self.monokai_theme()
        elif self.theme == "dracula":
            self.dracula_theme()
        elif self.theme == "tokyo_night":
            self.tokyo_night_theme()
        elif self.theme == "gruvbox":
            self.gruvbox_theme()
        elif self.theme == "nordic":
            self.nordic_theme()

    def light_theme(self):
        self.theme = "light"
        self.text_area.config(bg="white", fg="black", insertbackground="black")
        self.line_numbers.config(bg="lightgrey", fg="black")
        self.save_config()

    def dark_theme(self):
        self.theme = "dark"
        self.text_area.config(bg="black", fg="white", insertbackground="white")
        self.line_numbers.config(bg="grey", fg="white")
        self.save_config()

    def solarized_light_theme(self):
        self.theme = "solarized_light"
        self.text_area.config(bg="#fdf6e3", fg="#657b83", insertbackground="#657b83")
        self.line_numbers.config(bg="#eee8d5", fg="#586e75")
        self.save_config()

    def solarized_dark_theme(self):
        self.theme = "solarized_dark"
        self.text_area.config(bg="#002b36", fg="#839496", insertbackground="#839496")
        self.line_numbers.config(bg="#073642", fg="#586e75")
        self.save_config()

    def monokai_theme(self):
        self.theme = "monokai"
        self.text_area.config(bg="#272822", fg="#f8f8f2", insertbackground="#f8f8f2")
        self.line_numbers.config(bg="#3e3d32", fg="#75715e")
        self.save_config()

    def dracula_theme(self):
        self.theme = "dracula"
        self.text_area.config(bg="#282a36", fg="#f8f8f2", insertbackground="#f8f8f2")
        self.line_numbers.config(bg="#44475a", fg="#6272a4")
        self.save_config()

    def tokyo_night_theme(self):
        self.theme = "tokyo_night"
        self.text_area.config(bg="#1a1b26", fg="#c0caf5", insertbackground="#c0caf5")
        self.line_numbers.config(bg="#16161e", fg="#3d59a1")
        self.save_config()

    def gruvbox_theme(self):
        self.theme = "gruvbox"
        self.text_area.config(bg="#282828", fg="#ebdbb2", insertbackground="#ebdbb2")
        self.line_numbers.config(bg="#3c3836", fg="#d5c4a1")
        self.save_config()

    def nordic_theme(self):
        self.theme = "nordic"
        self.text_area.config(bg="#2E3440", fg="#D8DEE9", insertbackground="#D8DEE9")
        self.line_numbers.config(bg="#3B4252", fg="#D8DEE9")
        self.save_config()

    def on_content_changed(self, event=None):
        self.update_line_numbers()
        self.update_scroll_position()

    def update_line_numbers(self):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)

        line_count = int(self.text_area.index('end-1c').split('.')[0])
        line_number_content = "\n".join(map(str, range(1, line_count + 1)))
        self.line_numbers.insert(tk.END, line_number_content)

        self.line_numbers.config(state='disabled')

    def update_scroll_position(self):
        self.line_numbers.yview_moveto(self.text_area.yview()[0])

    def show_about(self):
        messagebox.showinfo("About", "note v0.0.1")

    def exit_application(self):
        self.root.destroy()

    def save_config(self):
        config = {"theme": self.theme}
        with open(self.config_file, "w") as file:
            json.dump(config, file)

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as file:
                config = json.load(file)
                self.theme = config.get("theme", "light")
        self.apply_theme()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
