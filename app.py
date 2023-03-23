from flask import Flask, render_template, request
import surfsender as ss

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text

# def main(url):
#     html = ss.html_retriever(url)
#     for i in ss.extract_all_surf_data(html):
#         print(i)

if __name__ == "__main__":
    url = my_form_post()
    # print(url)
    # html = ss.html_retriever(url)
    # for i in ss.extract_all_surf_data(html):
    #     print(i)
    # main(url)