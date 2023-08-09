#!/usr/bin/env python3
# ChangeImage.py
import os, sys
from PIL import Image

user = os.gatenv("USER")  # to get the username to environment variable
image_directory = "/home/{}/supplier-data/images/".format(user)
for image_name in os.listdir(image_directory):
    if not image_name.startswith(".") and "tiff" in image_name:
        image_path = image_directory + image_name
        path = os.path.splitext(image_path)[0]
        im = Image.open(image_path)
        new_path = "{}.jpeg".format(path)
        im.convert("RGB").resize((600, 400)).save(new_path, "JPEG")


#!/usr/bin/env python3
# upload images to web server
import requests, os

# the URL to upload the images
url = "http://localhost/upload/"
# To get the username from environment variable
USER = os.getenv("USER")
# The directory which contains all the images.
image_directory = "/home/{}/supplier-data/images/".format(USER)
# Listing all the files in images directory
files = os.listdir(image_directory)
# Parsing through all the images
for image_name in files:
    # Accepting files that has jpeg extension and ignoring hidden files
    if not image_name.startswith(".") and "jpeg" in image_name:
        # creating absolute path for each image
        image_path = image_directory + image_name
        # uploading jpeg files
        with open(image_path, "rb") as opened:
            r = requests.post(url, files={"file": opened})

#!/usr/bin/env python3
#uploading the description

import os, requests, json

def catalog_data(url, description_dir):
    """This function will return a list of dictionaries with all the details li$
        It will change the weight to integer format.
    """
    fruit = {}
    for item in os.listdir(description_dir):
        fruit.clear()
        filename=os.path.join(description_dir, item)
        with open(filename) as f:
            line = f.readlines()
            description = ""
            for i in range(2, len(line)):
                description = description+line[i].strip('\n').replace(u'\xa0',u$
            fruit["description"] = description
            fruit["weight"] = int(line[1].strip('\n').strip('lbs'))
            fruit["name"] = line[0].strip('\n')
            fruit["image_name"] = (item.strip('.txt'))+'.jpeg'
            print(fruit)
            if url!="":
                response = requests.post(url, json = fruit)
                print(response.request.url)
                print(response.status_code)
    return 0

if __name__ == '__main__':
    url = 'http://localhost/fruits/'
    user = os.gatenv('USER')
    description_directory = '/home/{}/supplier-data/descriptions/'.format(user)
    catalog_data(url, description_directory)


#!/usr/bin/env python3
#reports.py
from reportlab.platypus import Paragraph, Spacer, Image, SimpleDocTemptlate
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(file, title, add_info):
    styles = getSampleStyleSheet()
    report = SimpleDocTemplate(file)
    report_title = Paragraph(title, styles['h1'])
    report_info = Paragraph(add_info, styles['BodyText'])
    empty_line = Spacer(1, 20)

    report.build([report_title, empty_line, report_info, empty_line])


#!/usr/bin/env python3
#report_email.py

import datetime
import os

from run import catalog_data
from reports import generate_report
from emails import generate_email, send_email


def pdf_body(input_for, desc_dir):
    """Generating a summary with two lists, which gives the output name and weight"""
    res = []
    wt = []
    for item in os.listdir(desc_dir):
        filename = os.path.join(desc_dir, item)
        with open(filename) as f:
            line = f.readlines()
            weight = line[1].strip('\n')
            name = line[0].strip('\n')
            print(name, weight)
            res.append('name: ' +name)
            wt.append('weight: ' +weight)
            print(res)
            print(wt)
    new_obj = "" #initializing the object
    # Calling values from two lists one by one.
    for i in range(len(res)):
        if res[i] and input_for == 'pdf':
            new_obj +=res[i] + '<br />' + wt[i] + '<br />' + '<br />'
    return new_obj

if __name__ == "__main__":
    user = os.getenv('USER')
    descriptiong_directory = '/home/{}/supplier-data/descriptions/'.format(user)
    current_date = datetime.date.today().strftime('%B %d, %Y') #Creating data in format
    title = 'Processed Update on ' + str(current_date)
    generate_report('/tmp/processed.pdf', title, pdf_body('pdf', descriptiong_directory))
    email_subject = 'Upload Completed - Online Fruit Store'
    email_body = 'All fruits are uploaded to our website successfully. A detailed list is attached to this email.
    msg = generate_email('automation@example.com', '<username>@example.com'.format(user), email_subject, email_body, "/tmp/processed.pdf")
    send_email(msg)
