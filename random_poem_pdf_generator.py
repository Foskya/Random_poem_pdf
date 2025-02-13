import requests
import json
import random
from fpdf import FPDF

def random_poem():
    def API_random_author():
        response_json = requests.get("https://poetrydb.org/author")
        data_dictionary = json.loads(response_json.text)
        authors_list = data_dictionary['authors']
        random_author = random.choice(authors_list)
        return random_author

    def API_random_title(author): 
        response_json = requests.get(f"https://poetrydb.org/author/{author}/title")
        data_dictionary = json.loads(response_json.text)
        random_poem_title = random.choice(data_dictionary)
        random_title = random_poem_title['title']
        return random_title

    def API_poem_lines_list(author, title):
        response_json = requests.get(f"https://poetrydb.org/author,title/{author};{title}")
        data_dictionary = json.loads(response_json.text)
        lines_list = data_dictionary[0]['lines']
        return "\n".join(lines_list)

    author = API_random_author()
    title = API_random_title(author)
    text = API_poem_lines_list(author, title)
    return author, title, text

def pdf_creation(author, title, text):
    pdf = FPDF()
    pdf.add_page()
    # TITLE
    pdf.set_font("Courier", style="B",  size=12)
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)
    # TEXT
    pdf.set_font("Courier", size=10)
    pdf.multi_cell(0, 5, text)
    pdf.output(f"{author}.pdf")

def main():
    nr_of_documents = input("How many documents do you want to create?\n")
    i = 1
    while i < int(nr_of_documents)+1:
        try:
            author, title, text = random_poem()
            pdf_creation(f"{i} - {author}", title, text)
            print(f"{i} - {author} done")
            i+=1
        except:
            pass
    print("done")

if __name__ == "__main__":
    main()