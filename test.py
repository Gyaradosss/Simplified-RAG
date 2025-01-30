from langchain.text_splitter import RecursiveCharacterTextSplitter
text = "My favorite pet is a cat."
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=300, 
    chunk_overlap=50)

splits = text_splitter.split_text(text)
print(len(splits))