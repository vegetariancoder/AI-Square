
from langchain_community.document_loaders import Docx2txtLoader


# Load a document based on its file extension
def load_document(file_path):
    # If the file is a Word Doc, use Docx2txtLoader to read it
    if file_path.endswith(".docx"):
        word_loader = Docx2txtLoader(file_path)
        return word_loader.load()

    # Return a message if the file type is not supported
    return "File type not supported."



# print(load_document("/Users/sahilnagpal/Desktop/AI-Square/Project/Company_Assistant/data/CompanyWFH.docx"))