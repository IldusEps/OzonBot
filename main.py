from pypdf import PdfWriter, PdfReader, PageObject
import requests
import datetime
import dataBase
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

headers = {
    "Client-Id": os.getenv("CLIENT_ID"),
    "Api-Key": os.getenv("API_KEY"),
    "Content-Type": "application/json"
}


def get_bar_code(numbers):
    if numbers == []:
        return False

    data = {
        "posting_number": numbers
    }
    res = requests.post(
        "https://api-seller.ozon.ru/v2/posting/fbs/package-label", json=data, headers=headers)

    print(res.status_code)
    if res.status_code == 200:
        with open('metadata.pdf', 'wb') as f:
            f.write(res.content)
        return True
    else:
        print("Ошибка")
        return False


def get_awaiting_deliver():
    data = {
        "dir": "ASC",
        "filter": {
            "cutoff_from": "2021-08-24T14:15:22Z",
            "cutoff_to": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "delivery_method_id": [],
            "is_quantum": False,
            "provider_id": [],
            "status": "awaiting_deliver",
            "warehouse_id": []
        },
        "limit": 1000,
        "offset": 0
        # "with": {
        #     "barcodes": True
        # }
    }
    res = requests.post(
        "https://api-seller.ozon.ru/v3/posting/fbs/unfulfilled/list", json=data, headers=headers)

    print(res.status_code)
    if res.status_code == 200:
        res = res.json()
        numbers = []
        for post in res["result"]["postings"]:
            numbers.append(post["posting_number"])

        return numbers
    else:
        print("Ошибка")
        print(res.json())
        return []


def create_pdf_file(first_rows=True):
    if get_bar_code(get_awaiting_deliver()) == False:
        return False

    input1 = PdfReader(open("metadata.pdf", "rb"), strict=False)

    margin_x = 40
    margin_y = 20

    max_x_count = 5
    max_y_count = 5
    max_count = max_y_count * max_x_count

    # total_width = page1.mediaBox.upperRight[0] + page2.mediaBox.upperRight[0]
    total_width = 1240
    total_height = 1754
    # total_height = max([page1.mediaBox.upperRight[1],
    #                    page2.mediaBox.upperRight[1]])

    new_page = PageObject.create_blank_page(None, total_width, total_height)
    output = PdfWriter()

    y_source, x_source, droping = dataBase.get_unfilled(first_rows)
    y, x = y_source, x_source
    offset = 0

    for page in input1.pages:
        if (x + 1) * (y + 1) > max_count:
            output.add_page(new_page)
            new_page = PageObject.create_blank_page(
                None, total_width, total_height)
            x = 0
            y = 0
            offset = 0
            dataBase.data_clear()
        # page.rotate(-90)
        # page.transfer_rotation_to_content()

        if first_rows:
            if x == max_x_count:
                y += 1
                x = 0
        else:
            if y == max_y_count:
                x += 1
                y = 0

        if first_rows and y == y_source and y == max_y_count - 1:
            new_page.merge_translated_page(
                page, margin_x + (page.mediabox.upper_right[0] + 20) * offset,  margin_y + (page.mediabox.upper_right[1]) * y)
            offset += 1
        elif first_rows is False and x == x_source and x == max_x_count - 1:
            new_page.merge_translated_page(
                page, margin_x + (page.mediabox.upper_right[0] + 20) * x,  margin_y + (page.mediabox.upper_right[1]) * offset)
            offset += 1
        else:
            new_page.merge_translated_page(
                page, margin_x + (page.mediabox.upper_right[0] + 20) * x,  margin_y + (page.mediabox.upper_right[1]) * y)
        dataBase.dataA4[y][x] = 1
        if first_rows:
            x += 1
        else:
            y += 1

    print(dataBase.dataA4)
    output.add_page(new_page)
    output.write(open("result.pdf", "wb"))
    dataBase.data_save()
    return True, droping


def create_count_pdf(count):
    input1 = PdfReader(open("metadata copy.pdf", "rb"), strict=False)

    output = PdfWriter()
    for page in range(0, count):
        output.add_page(input1.pages[page % 2])
    output.write(open("metadata.pdf", "wb"))


# create_count_pdf(7)
