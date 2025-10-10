# get main language code from text using cld2
def detect_language(text: str="") -> str:
    is_reliable, text_bytes_found, details = cld2.detect(text)
    if is_reliable:
        return details[0][1]
    return "en"


def get_abstract_from_gotriple_id(id: str="", lang: str="en") -> str:
    # build the URL and get the resource
    url = f"https://www.gotriple.eu/documents/{ quote_plus(id) }"
    return get_abstract_from_gotriple_url(url, lang)

# parse language-specific abstract from GoTriple URL request response
def get_abstract_from_gotriple_url(url: str="", lang: str="en") -> str:
    response = requests.get(url, timeout=30)
    # parse out the tag containing abstracts from the response 
    soup = BeautifulSoup(response.text, features="html.parser")
    tag = soup.find("script", id="__NEXT_DATA__")
    if tag:
        # parse language-specific abstract text from the contents of this tag
        meta = json.loads(str(tag.contents[0]))
        abstracts = meta.get("props", {}).get("pageProps", {}).get("document", {}).get("abstract", [])        
        abstract = next(filter(lambda a: a.get("lang", "") == lang, abstracts), {}).get("text", "")
        return str(abstract).strip()
    return ""




