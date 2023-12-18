import os
import tkinter as tk
from tkinter import filedialog
from unittest import TestCase
import seaborn as sns
import matplotlib.pyplot as plt
import torch
from PyPDF2 import PdfFileReader

class CustomPdfHarvester:

    def __init__(self):
        self.title = None
        self.content = None

    def harvest_file(self, file_path):
        with open(file_path, 'rb') as file:
            pdf_reader = PdfFileReader(file)
            text_content = ""
            for page_num in range(pdf_reader.numPages):
                text_content += pdf_reader.getPage(page_num).extractText()

        
        lines = text_content.split('\n')
        self.title = lines[0].strip()

       
        self.content = '\n'.join(lines[1:]).strip()

        return {'title': self.title, 'content': self.content}


class TestCustomPdfHarvester(TestCase):

    def test_custom_basics(self):
        path = os.path.join(os.path.dirname('.'), 'test.pdf')
        custom_harvester = CustomPdfHarvester()
        result = custom_harvester.harvest_file(path)
        self.assertEqual(result['title'], "The title")
        self.assertEqual(result['content'], "This is the content with a diacritic: à.")


def select_file():
    file_selected = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_selected:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_selected)

def harvest_and_display():
    file_path = entry_path.get()
    if not file_path.endswith('.pdf'):
        status_label.config(text="Selected file is not a PDF.")
        return

    harvester = CustomPdfHarvester()
    result = harvester.harvest_file(file_path)
    title_label.config(text=f"Title: {result['title']}")
    content_text.delete(1.0, tk.END)
    content_text.insert(tk.END, f"Content: {result['content']}")
    status_label.config(text="PDF harvested successfully.")


root = tk.Tk()
root.title("PDF Harvester with GUI")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=20, pady=20)

label_path = tk.Label(frame, text="Select PDF File:")
label_path.grid(row=0, column=0, sticky='e')

entry_path = tk.Entry(frame, width=50)
entry_path.grid(row=0, column=1, padx=5)

button_browse = tk.Button(frame, text="Browse", command=select_file)
button_browse.grid(row=0, column=2, padx=5)

button_harvest = tk.Button(frame, text="Harvest", command=harvest_and_display)
button_harvest.grid(row=1, column=1, pady=10)

title_label = tk.Label(frame, text="")
title_label.grid(row=2, column=0, columnspan=3, pady=5)

content_text = tk.Text(frame, height=10, width=60)
content_text.grid(row=3, column=0, columnspan=3, pady=5)

status_label = tk.Label(frame, text="")
status_label.grid(row=4, column=0, columnspan=3, pady=5)

ns.set(style="whitegrid")


torch_tensor = torch.randn(100)

sns.lineplot(x=range(len(torch_tensor)), y=torch_tensor.numpy())
plt.title('Seaborn Plot of Torch Tensor')
plt.show()

root.mainloop()
