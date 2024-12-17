import os
import PyPDF2

file_path = "supporting_resources/attention-is-all-you-need.pdf"


if os.path.exists(file_path):
    print(f"File '{file_path}' found.")
else:
    print(f"Error: File '{file_path}' not found.")
with open(file_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    number_of_pages = len(reader.pages)
    print(f"The PDF file has {number_of_pages} pages.")
