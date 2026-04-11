from langchain_text_splitters import MarkdownHeaderTextSplitter,CharacterTextSplitter
from Project.Company_Assistant.ingestion.loader import load_document


def markdown_split_document(file_path):
    md_text_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ('#', 'Section'),
            ('##', 'SubSection')
        ]
    )


    return md_text_splitter.split_text(file_path)

def character_split_document(file_path):
    md_split_doc = markdown_split_document(file_path[0].page_content)

    print("Total Pages: ", len(md_split_doc))
    print("The Length of the split document is: ", len(md_split_doc[0].page_content))

    for content in md_split_doc:
        content.page_content = content.page_content.replace("\n", " ")

    ch_text_splitter = CharacterTextSplitter(chunk_size=500,
                                             chunk_overlap=0,
                                             separator=".")
    return ch_text_splitter.split_documents(file_path)



word_doc = load_document("/Users/sahilnagpal/Desktop/AI-Square/Project/Company_Assistant/data/CompanyWFH.docx")

md_split_doc = markdown_split_document(word_doc[0].page_content)

ch_split_doc = character_split_document(md_split_doc)