from flask import Flask, render_template, request, jsonify
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
import os
import openai
from langchain_openai import OpenAIEmbeddings

openai.api_key = os.getenv('OPENAI_KEY')
embd = OpenAIEmbeddings(openai_api_key=openai.api_key)
file_path = ("/home/ec2-user/myweb/doc.pdf")
loader = PyPDFLoader(file_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=10, 
    chunk_overlap=0)
splits = text_splitter.split_documents(docs)

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    messages = []
    if request.method == 'POST':
        query = request.get_json().get('user_input', '') 
        history = request.get_json().get('history', []) 
        vectorstore = Chroma.from_documents(documents=splits, 
                                    embedding=embd)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
        docs = retriever.get_relevant_documents(query)
        template = """Answer the question based only on the following context:{context}
                    Question: {question}"""
        final_prompt = template.format(context=docs,question=query)
        for message in history:
            messages.append(message)
        messages.append({"role": "user", "content": final_prompt})
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages = messages,
        )
        output = response.choices[0].message.content

    if request.is_json:
        return jsonify({'openai_response': output})
    return render_template('web.html', openai_response=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
    

    