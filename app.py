from flask import Flask,render_template,request
import os
import requests
import logging
import csv
from bs4 import BeautifulSoup
app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/review",methods=["POST","GET"])
def review():
    if request.method=="POST":
        try:
            query = request.form['content'].replace(" ","")


            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

            response = requests.get(f"https://www.flipkart.com/{query}/product-reviews/itm5d6e44f7fd976?pid=DLLFFNVDYGQN9XCS&lid=LSTDLLFFNVDYGQN9XCSYTRJDH&marketplace=FLIPKART")
            print(response)

            soup = BeautifulSoup(response.content, "html.parser")
            #print(soup)
            reviews=[]
            review_elements = soup.find_all('div', class_='_27M-vq')
            for i in review_elements:
                rating = i.find('div', class_='_3LWZlK').get_text()
                comment = i.find('div', class_='').get_text()
                title =i.find('p', class_='_2-N8zT').get_text()
                author= i.find('p', class_='_2sc7ZR').get_text()
                reviews.append([rating, comment,title,author])
            print(reviews)

            save_directory = "review"
            csv_path = f"{save_directory}/reviews.csv"

            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(['review_rating','review_comment','review_title','review_author'])
                writer.writerows(reviews)

            #return "review loaded"
            return render_template('result.html', output=reviews) 
        
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
            
    else:
        return render_template('index.html')
    




if __name__=="__main__":
    app.run(debug=True)