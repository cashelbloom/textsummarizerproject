# code that extracts text from a pdf file and sends generates a summary and keywords from the text
# import fitz
import PyPDF2
import openai
import sys
import secrets_from_secretsmanager

openai.api_key = secrets_from_secretsmanager.get_secret()


# Function to read the first page of a PDF and extract the abstract
def extract_abstract(pdf_path):

    # Open the PDF file and grab text from the 1st page
    with open(pdf_path) as pdf:
        reader = PyPDF2.PdfReader(pdf_path)
        number_of_pages = len(reader.pages)
        first_page = reader.pages[0]
        text = first_page.extract_text()

    # Extract the abstract (assuming the abstract starts with 'Abstract')

    # find where abstract starts
    start_idx = text.lower().find("abstract")

    # end abstract at introduction if it exists on 1st page
    if "introduction" in text.lower():
        end_idx = text.lower().find("introduction")
    else:
        end_idx = None

    # extract abstract text
    abstract = text[start_idx:end_idx].strip()

    # if abstract appears on 1st page return it, if not resturn None
    if start_idx != -1:
        abstract = text[start_idx:end_idx].strip()
        return abstract
    else:
        return None


# Function to summarize the abstract and generate keywords using OpenAI API
def summarize_and_generate_keywords(abstract):

    # Use OpenAI Chat Completions API to summarize and generate keywords
    prompt = f"Summarize the following paper abstract and generate (no more than 5) keywords:\n\n{abstract}"

    # make api call
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.25,
    )

    # extract response
    print(f"This is the data type of choice contents: {type(response.choices[0])}")
    print(f"This is the first choice contents: {response.choices[0]}")
    summary = response.choices[0].message.content
    return summary


def exec_summarizer(file_path):
    # Get the PDF path from the command-line arguments
    pdf_path = file_path  # sys.argv[1]
    print(f"filepath is: {pdf_path}")
    # Extract abstract from the PDF
    abstract = extract_abstract(pdf_path)

    # if abstract exists on first page, print summary.
    if abstract:
        # Summarize and generate keywords
        summary = summarize_and_generate_keywords(abstract)

        print(summary)
    else:
        print("Abstract not found on the first page.")


if __name__ == "__main__":
    print(f"This is the file path: {sys.argv[1]}")
    pdf_path = sys.argv[1]
    exec_summarizer(pdf_path)
# Get the PDF path from the command-line arguments
# print(f"This is the file path: {sys.argv[1]}")
# pdf_path = sys.argv[1]

# # Extract abstract from the PDF
# abstract = extract_abstract(pdf_path)

# # if abstract exists on first page, print summary.
# if abstract:
#     # Summarize and generate keywords
#     summary = summarize_and_generate_keywords(abstract)

#     print(summary)
# else:
#     print("Abstract not found on the first page.")
