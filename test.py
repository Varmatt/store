from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route('/')
def avecaesar():
    return 'Ave Caesar!'

with open('aboba.json', 'r') as file:
    data = json.load(file)




@app.route('/products', methods=['GET'])
def get_products():
    kv = {}
    for key, value in request.args.items():
        kv[key] = value

    filters = list(reversed(sorted(data['products'], key=lambda x: x['rating'])))
    if key_in_dictionary(kv, "sort_by"):
        if kv["sort_by"] == "price_down":
            filters = sorted(filters, key=lambda x: x['price'])
        elif kv["sort_by"] == "price_up":
            filters = list(reversed(sorted(filters, key=lambda x: x['price'])))
        elif kv["sort_by"] == "rating_down":
            filters = sorted(filters, key=lambda x: x['rating'])
        elif kv["sort_by"] == "alphabet":
            filters = sorted(filters, key=lambda x: x['title'])

    if key_in_dictionary(kv, "sku"):
        filters = list(filter(lambda p: p["sku"] == kv["sku"], filters))

    if key_in_dictionary(kv, "category"):
        filters = list(filter(lambda p: p["category"] == kv["category"], filters))

    if key_in_dictionary(kv, "tags"):
        filters = list(filter(lambda p: all([1 if i in str(p["tags"]) else 0 for i in kv["tags"].split(',')]), data["products"]))

    if key_in_dictionary(kv, "price_from"):
        filters = list(filter(lambda p: int(kv["price_from"]) <= int(p["price"]), filters))

    if key_in_dictionary(kv, "price_to"):
        filters = list(filter(lambda p: int(p["price"]) <= int(kv["price_to"]), filters))

    if key_in_dictionary(kv, "brand"):
        filters = list(filter(lambda p: "brand" in p and p["brand"] == kv["brand"], filters))

    return jsonify(filters)





def key_in_dictionary(dic, key):
    if key in list(dic.keys()):
        return True
    else:
        return False


def create_json():
    data = {
        "message": 'Ave Caesar1'
    }
    with open('data.json', 'w') as file:
        json.dump(data, file)
    return data


if __name__ == '__main__':
    app.run(debug=False, host="192.168.1.68")