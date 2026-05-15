from pypdf import PdfReader

input_file_name = "./data/journals_july_2024/078_047_054.pdf"
reader = PdfReader(input_file_name)
page = reader.pages[0]
text = page.extract_text(0)

parts = []

def visitor_body(text, cm, tm, font_dict, font_size):
    y = cm[5]
    if 27 < y < 208:
        parts.append(text)


page.extract_text(visitor_text=visitor_body)
text_body = "".join(parts)

print(text)