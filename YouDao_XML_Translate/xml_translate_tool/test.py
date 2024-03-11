import tkinter as tk

def scroll_to_bottom():
    text_box.yview_moveto(1.0)  # Scroll to the bottom

def add_text():
    content = text_entry.get()
    text_box.insert(tk.END, content + '\n')
    scroll_to_bottom()

# Create the main window
window = tk.Tk()

# Create a Text widget
text_box = tk.Text(window)
text_box.pack()

# Create an Entry widget for entering text
text_entry = tk.Entry(window)
text_entry.pack()

# Create a button to add the text
add_button = tk.Button(window, text="Add Text", command=add_text)
add_button.pack()

# Run the main window loop
window.mainloop()
