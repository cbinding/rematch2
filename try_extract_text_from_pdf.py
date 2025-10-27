# extracting text from a PDF file using pypdf
import argparse                         # for argument parsing
from pypdf import PdfReader


def extract_text_from_pdf(inputFileName: str = "", options={}) -> str:
    reader = PdfReader(inputFileName)
    content = map(lambda page: page.extract_text().strip(), reader.pages)
    text = "\n\n".join(content)
    #page = reader.pages[0] # only first page for now
    #text = page.extract_text().strip()    
    return text


# test the functions
if __name__ == "__main__":
    # set up command line arg parser
    parser = argparse.ArgumentParser(
        prog=__file__, description="Extract text from PDF file")

    # add long and short command line argument descriptions
    parser.add_argument("--inputfilename", "-i", required=False,
                        help="Input file name")

    parser.add_argument("--outputfilename", "-o", required=False,            
                        help="Output file name")

    # parse command line arguments
    args = parser.parse_args()

    # get clean required arguments
    inputFileName = "./data/journals_july_2024/078_047_054.pdf" # default for test
    outputFileName = ""
    
    if args.inputfilename:
        inputFileName = args.inputfilename.strip()
    if args.outputfilename:
        outputFileName = args.outputfilename.strip()
    else:
         outputFileName = f"{inputFileName}.txt"

    text = extract_text_from_pdf(inputFileName)
    #text = normalize_whitespace(text)
    print(text)

    with open(outputFileName, "w") as f:
        f.write(text)

