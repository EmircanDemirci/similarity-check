import tkinter as tk
from tkinter import filedialog
from difflib import SequenceMatcher


def compareText(text1,text2):
    d = SequenceMatcher(None , text1,text2) #using this class for compare we set the custom comparison function to None to use default comparision
    similarity_ratio = d.ratio()
    similarity_percentage = int(similarity_ratio*100)

    diff = list(d.get_opcodes())#this return is like [('insert', 0, 0, 0, 7), ('equal', 0, 2, 7, 9), ...]
    return similarity_percentage , diff

def show_similarity():
    text1 = text_widget.get(1.0,tk.END)#get all text
    text2 = text_widget2.get(1.0 , tk.END)
    similarity_percentage , diff = compareText(text1, text2)
    similarity_text.delete(1.0,tk.END)
    similarity_text.insert(tk.END,f"Similarity:{similarity_percentage}%")
    
    text_widget.tag_remove("same" , "1.0" , tk.END)#remove tag in text widget
    text_widget2.tag_remove("same" , "1.0" , tk.END)
    text_widget.tag_remove("replace" , "1.0" , tk.END)#remove tag in text widget
    text_widget2.tag_remove("replace" , "1.0" , tk.END)

    for opcode in diff:
        #this elements looks like ('equal', 0, 2, 7, 9) this
        tag = opcode[0]
        start1 = opcode[1]
        end1 = opcode[2]
        start2 = opcode[3]
        end2 = opcode[4]

        if tag == "equal":
            #we add same tag to equal elements for highlight
            text_widget.tag_add("same" , f"1.0+{start1}c" , f"1.0+{end1}c")
            text_widget2.tag_add("same" , f"1.0+{start2}c" , f"1.0+{end2}c")

def open_file(entry_widget, text_widget):
    file_path = filedialog.askopenfilename(
        title="Select a Text File", filetypes=[("Text files", "*.txt")])

    if file_path:
        with open(file_path, "r", encoding='utf-8') as file:
            content = file.read()
            entry_widget.delete(0, tk.END)
            entry_widget.insert(tk.END, file_path)
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, content)

# create root window
root = tk.Tk()
root.title("Plagiarism Detect")

# get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# set window size and position
window_width = int(screen_width * 0.6)
window_height = int(screen_height * 0.6)
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# frame1 for text and open file widgets
frame1 = tk.Frame(root)
frame1.grid(row=0, column=0, padx=10, pady=10)
frame2 = tk.Frame(root)
frame2.grid()

# label for first widget
label_widget = tk.Label(frame1, text="First Data:")
label_widget.grid(row=0, column=0, padx=10, pady=5)

# text widget to display the content
text_widget = tk.Text(frame1, wrap="word")
text_widget.grid(row=1, column=0, padx=10, pady=10)

# entry for first textline
entry_widget = tk.Entry(frame1)
entry_widget.grid(row=2, column=0, padx=10, pady=10)

# button to open the file for first text widget
open_button = tk.Button(frame1, text="Open File", command=lambda: open_file(entry_widget=entry_widget, text_widget=text_widget))
open_button.grid(row=3, column=0, padx=10, pady=10)


# label for second widget
label_widget2 = tk.Label(frame1, text="Second Data:")
label_widget2.grid(row=0, column=1, padx=10, pady=5)

# text widget for second content
text_widget2 = tk.Text(frame1, wrap="word")
text_widget2.grid(row=1, column=1, padx=10, pady=10)

# entry for second textline
entry_widget2 = tk.Entry(frame1)
entry_widget2.grid(row=2, column=1, padx=10, pady=10)

# button to open the file for second text widget
open_button2 = tk.Button(frame1, text="Open File", command=lambda: open_file(entry_widget=entry_widget2, text_widget=text_widget2))
open_button2.grid(row=3, column=1, padx=10, pady=10)


#button for frame2
compare_button = tk.Button(frame2, text="Compare" ,command=show_similarity)
compare_button.grid(pady=10)

#similarity percentage text
similarity_text = tk.Text(frame2 , wrap=tk.WORD, width=80, height=1)
similarity_text.grid(pady=10)


#highlight same elements
text_widget.tag_configure("same", foreground="red", background="lightyellow")
text_widget2.tag_configure("same", foreground="red", background="lightyellow")


root.mainloop()