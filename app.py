import streamlit as st
import requests
import json
import base64
import mysql.connector
import os                                                                                                                                                                                                          
from dotenv import load_dotenv, find_dotenv
from dotenv.main import load_dotenv
from pathlib import Path
load_dotenv()
key=os.environ["api_key"]
host=os.environ["host"]
user=os.environ["user"]
password=os.environ["password"]
database=os.environ["database"]
url=os.environ["url"]
sets=os.environ["sets"]
connection = mysql.connector.connect(
  host=host,
  user=user,
  password=password,
  database=database
)
endpoint =str(url)+"?key="+key
headers = {"Content-Type": "application/json; charset=utf-8"}
# Allow the user to select an image file
# Allow the user to select an image file
def get_base64_data(image_file):
    # Read the image file as binary data
    image_data = image_file.getvalue()

    # Encode the binary data as a base64-encoded string
    base64_data = base64.b64encode(image_data).decode()

    return base64_data

# Allow the user to select an image file
image_file = st.file_uploader("Select an image file:")
if image_file is not None:
    # Call the get_base64_data function and assign its return value to a variable
    base64_data = get_base64_data(image_file)
basedata=base64_data
request_body = {
  "requests": [
    {
      "image": {
        "content":basedata
        },
      
      "features": [
        {
          "type": "PRODUCT_SEARCH",
          "maxResults": 5
        }
      ],
      "imageContext": {
        "productSearchParams": {
          "productSet": sets,
          "productCategories": [
               "apparel-v2"
          ]
        }
      }
    }
  ]
}

if st.button("Submit"):
    response = requests.post(endpoint, json=request_body, headers=headers)
    # Parse the JSON response
    response_data = response.json()

    # Get the first response in the "responses" field
    first_response = response_data["responses"][0]

    # Get the "productSearchResults" field from the response
    product_search_results = first_response["productSearchResults"]

    # Get the first result in the "results" field
    first_result = product_search_results["results"][0]

    # Get the "product" field from the result
    product = first_result["product"]

    # Get the "name" field from the product
    matchfound = product["name"]

    # Parse the JSON response
    response_data = response.json()

    # Get the first response in the "responses" field
    first_response = response_data["responses"][0]

    # Get the "productSearchResults" field from the response
    product_search_results = first_response["productSearchResults"]

    # Get the first result in the "results" field
    first_result = product_search_results["results"][0]

    # Get the "score" field from the result
    score = first_result["score"]
    
    matchfound=matchfound

    cursor = connection.cursor()
    query = "SELECT title, image, price, size FROM products WHERE reference = %s"
    # Pass the query string and the value for the parameter as separate arguments to the cursor.execute() method
    cursor.execute(query, (matchfound,))
    results = cursor.fetchall()
    for row in results:
        title, image, price, size = row
    # Define the card content as a string of HTML and CSS
        # Define the card content as a string of HTML and CSS
        card_content = """
        <div style="border: 1px solid black; padding: 20px;">
        <h1>{title}</h1>
        <img src="{image}"  style="width: 200px; height: auto;">
        <p>Price: {price}</p>
        <p>Size: {size}</p>
        </div>
        """.format(title=title, image=image, price=price, size=size)

        # Use the st.markdown() function to render the card content
        st.markdown(card_content, unsafe_allow_html=True)




