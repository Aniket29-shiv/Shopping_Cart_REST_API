from flask import Flask, make_response, request, jsonify
from api_constants import mongodb_password
from flask_mongoengine import MongoEngine

app = Flask(__name__)

database_name = "API"
password = mongodb_password
DB_URI = "mongodb+srv://Aniket2971:{}@cluster0.yso2i.mongodb.net/{}?retryWrites=true&w=majority".format(password, database_name)
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)

'''
Sample Request Body
{
    "item_id" : 1,
    "name" : "Watch",
    "manufacturer" : "Rolex"
}

'''

class Item(db.Document):
    item_id = db.IntField()
    name = db.StringField()
    manufacturer = db.StringField()

    def to_json(self):
        #converts this document to JSON
        return {
            "item_id" : self.item_id,
            "name" : self.name,
            "manufacturer" : self.manufacturer
        }

'''
>>> HTTP Methods for our API

POST /api/db_populate -> Populates the db and returns 201 success code

GET /api/items -> Returns the details of all items

POST /api/items -> Create a new item and returns 201 success code

GET /api/items/3 -> Returns the details of item 3

PUT /api/items/3 -> Updates the manufacturer and name fields of item 3

DELETE /api/items/3 -> Deletes item 3 

'''

@app.route('/api/db_populate', methods = ['POST'])
def db_populate():
    item1 = Item(item_id=1, name="Watch", manufacturer = "Rolex")
    item2 = Item(item_id=2, name="Shoes", manufacturer = "Nike")
    item3 = Item(item_id=3, name="Fan", manufacturer = "Bajaj")
    item4 = Item(item_id=4, name="Milk", manufacturer = "Amul")
    item1.save()
    item2.save()
    item3.save()
    item4.save()
    return make_response("", 201)

@app.route('/api/items', methods = ['GET','POST'])
def api_items():
    if request.method == "GET":
        items = []
        for item in Item.objects:
            items.append(item)
        return make_response(jsonify(items), 200)
    elif request.method == "POST":
        content = request.json
        item = Item(item_id=content['item'],name=content['name'],manufacturer=content['manufacturer'])
        item.save()

@app.route('/api/items/<item_id>', methods = ['GET','PUT','DELETE'])
def api_each_item(item_id):
    if request.method == "GET":
        item_obj = Item.objects(item_id=item_id).first()
        if item_obj:
            return make_response(jsonify(item_obj.to_json()), 200)
        else:
            return make_response("", 404)

    elif request.method == "PUT":
        '''
        Sample Request Body
        {
            "item_id" : 1,
            "name" : "Watch",
            "manufacturer" : "Rolex"
        }

        '''
        content = request.json
        item_obj = Item.objects(item_id=item_id).first()
        item_obj.update(manufacturer=content['manufacturer'], name=content['name'])
        return make_response("", 204)

    elif request.method == "DELETE":
        item_obj = Item.objects(item_id=item_id).first()
        item_obj.delete()
        return make_response("", 204)


# Main function
if __name__ == '__main__':
    app.run(debug= True)