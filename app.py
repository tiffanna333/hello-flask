from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
# creates a new instance of Flask stored inside of the variable

basedir = os.path.abspath(os.path.dirname(__file__))
# tells flask in our server or environment where the file is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
# this has to be set just like this or it doesn't work. Is in the system.
# last piece names the database and can be changed per project
db = SQLAlchemy(app)
# database object
ma = Marshmallow(app)
# marshmallow object

class Guide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    content = db.Column(db.String(144), unique=False)
# Guide inherits from the database object model.
# added a new column w/ type of integer and it's a primary key.
# Primary key makes sure it has a unique ID and the ID will automatically increment w/ each new ID created
# String(#) tells max characters allowed for those parts.

    def __init__(self, title, content):
        self.title = title
        self.content = content


class GuideSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content')
# allows access to the fields title and content
# adds structure to the database


guide_schema = GuideSchema()
guides_schema = GuideSchema(many=True)

# Endpoint to create a new guide
@app.route('/guide', methods=["POST"])
# tells where to place what's created and what to do with it
def add_guide():
    title = request.json['title']
    content = request.json['content']

    new_guide = Guide(title, content)
    # uses Guide class

    db.session.add(new_guide)
    # creates new db session and adds new guide into it
    db.session.commit()
    # commit is in SQLAlchemy that says to save the new guide

    guide = Guide.query.get(new_guide.id)
    # get expects id in the table

    return guide_schema.jsonify(guide)


# Endpoint to query all guides
@app.route("/guides", methods=["GET"])
def get_guides():
    all_guides = Guide.query.all()
    result = guides_schema.dump(all_guides)
    return jsonify(result)


# Endpoint for querying a single guide
@app.route("/guide/<id>", methods=["GET"])
def get_guide(id):
    guide = Guide.query.get(id)
    return guide_schema.jsonify(guide)
# the <> make what's in them available to the function


# Endpoing for updating a guide
@app.route("/guide/<id>", methods=["PUT"])
def guide_update(id):
    guide = Guide.query.get(id)
    title = request.json['title']
    content = request.json['content']

    guide.title = title
    guide.content = content

    db.session.commit()
    return guide_schema.jsonify(guide)
# a different http verb triggers a different action even with same route
# this expects both title and content to update
# will look at how to update one or the other at a later point 


# Endpoint for deleting a record
@app.route("/guide/<id>", methods=["DELETE"])
def guide_delete(id):
    guide = Guide.query.get(id)
    db.session.delete(guide)
    db.session.commit()

    # return guide_schema.jsonify(guide)
    return f"Guide {id} was successfully deleted."
# You don't have to return the guide, you can return anything.


if __name__ == '__main__':
    app.run(debug=True)