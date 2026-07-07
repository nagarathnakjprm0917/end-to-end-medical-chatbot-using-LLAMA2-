          (in gitbash)
 git clone https://github.com/nagarathnakjprm0917/end-to-end-medical-chatbot-using-LLAMA2-.git
cd end-to-end-medical-chatbot-using-LLAMA2-/
 code .
 conda create -n mchatbot python=3.10.20 -y
  conda activate mchatbot
  pip install -r requirement.txt

***
  (in git bash check for which environment you are doing in conda or venv environment:
  echo $VIRTUAL_ENV
  echo $CONDA_PREFIX
  )***


  @app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]

    result = qa.invoke({"query": msg})

    print(result["result"])

    return result["result"]

    Techstack Used:
Python
LangChain
Flask
Meta Llama2
Pinecone

