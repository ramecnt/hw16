import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
with app.app_context():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    db = SQLAlchemy(app)


    class User(db.Model):
        __tablename__ = 'user'

        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String)
        last_name = db.Column(db.String)
        age = db.Column(db.Integer)
        email = db.Column(db.String)
        role = db.Column(db.String)
        phone = db.Column(db.String)

        def to_dict(self):
            return {
                "id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "age": self.age,
                "email": self.email,
                "role": self.role,
                "phone": self.phone,
            }


    class Offer(db.Model):
        __tablename__ = 'offer'

        id = db.Column(db.Integer, primary_key=True)
        order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
        executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
        user = db.relationship("User")
        order = db.relationship("Order")

        def to_dict(self):
            return {
                "id": self.id,
                "order_id": self.order_id,
                "executor_id": self.executor_id,
            }


    class Order(db.Model):
        __tablename__ = 'order'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String)
        description = db.Column(db.String)
        start_date = db.Column(db.String)
        end_date = db.Column(db.String)
        address = db.Column(db.String)
        price = db.Column(db.Integer)
        customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
        executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
        customer = db.relationship("User", foreign_keys=[customer_id])
        executor = db.relationship("User", foreign_keys=[executor_id])

        def to_dict(self):
            return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "address": self.address,
                "price": self.price,
                "customer_id": self.customer_id,
                "executor_id": self.executor_id,
            }


    db.create_all()

    with open("data/users.json", "r", encoding="utf-8") as users:
        for i in json.load(users):
            user = User(first_name=i["first_name"],
                        last_name=i["last_name"],
                        age=i["age"],
                        email=i["email"],
                        role=i["role"],
                        phone=i["phone"])
            db.session.add(user)
            db.session.commit()

    with open("data/offers.json", "r", encoding="utf-8") as offers:
        for i in json.load(offers):
            offer = Offer(order_id=i["order_id"],
                          executor_id=i["executor_id"])
            db.session.add(offer)
            db.session.commit()

    with open("data/orders.json", "r", encoding="utf-8") as orderse:
        for i in json.load(orderse):
            order = Order(name=i["name"],
                          description=i["description"],
                          start_date=i["start_date"],
                          end_date=i["end_date"],
                          address=i["address"],
                          price=i["price"],
                          customer_id=i["customer_id"],
                          executor_id=i["executor_id"]
                          )
            db.session.add(order)
            db.session.commit()


    @app.route('/users', methods=['POST', 'GET'])
    def all_users():
        if request.method == 'GET':
            result = []
            for i in User.query.all():
                result.append(i.to_dict())
            return jsonify(result)
        elif request.method == 'POST':
            user_raw = json.loads(request.data)
            user = User(first_name=user_raw["first_name"],
                        last_name=user_raw["last_name"],
                        age=user_raw["age"],
                        email=user_raw["email"],
                        role=user_raw["role"],
                        phone=user_raw["phone"])
            db.session.add(user)
            db.session.commit()
            return "новый пользователь записан"


    @app.route('/users/<x>', methods=['PUT', 'DELETE', 'GET'])
    def one_user(x):
        if request.method == 'GET':
            return jsonify(User.query.get(x).to_dict())
        elif request.method == 'DELETE':
            user = User.query.get(x)
            db.session.delete(user)
            db.session.commit()
            return "пользователь удален"
        elif request.method == 'PUT':
            user_new = json.loads(request.data)
            user = User.query.get(x)
            user.id = user_new['id']
            user.first_name = user_new["first_name"]
            user.last_name = user_new["last_name"]
            user.age = user_new['age']
            user.email = user_new['email']
            user.role = user_new['role']
            user.phone = user_new['phone']
            db.session.add(user)
            db.session.commit()
            return 'новые данные о пользователе записаны'


    @app.route('/orders', methods=['POST', 'GET'])
    def all_orders():
        if request.method == 'GET':
            result = []
            for i in Order.query.all():
                result.append(i.to_dict())
            return jsonify(result)
        elif request.method == 'POST':
            order_raw = json.loads(request.data)
            order = Order(name=order_raw["name"],
                          description=order_raw["description"],
                          start_date=order_raw["start_date"],
                          end_date=order_raw["end_date"],
                          address=order_raw["address"],
                          price=order_raw["price"],
                          customer_id=order_raw["customer_id"],
                          executor_id=order_raw["executor_id"]
                          )
            db.session.add(order)
            db.session.commit()
            return "новый заказ записан"


    @app.route('/orders/<x>', methods=['PUT', 'DELETE', 'GET'])
    def one_order(x):
        if request.method == 'GET':
            return jsonify(Order.query.get(x).to_dict())
        elif request.method == 'DELETE':
            order = Order.query.get(x)
            db.session.delete(order)
            db.session.commit()
            return 'заказ удален'
        elif request.method == 'PUT':
            order_new = json.loads(request.data)
            order = Order.query.get(x)
            order.id = order_new['id']
            order.name = order_new["name"]
            order.description = order_new["description"]
            order.start_date = order_new["start_date"]
            order.end_date = order_new["end_date"]
            order.address = order_new["address"]
            order.price = order_new["price"]
            order.customer_id = order_new["customer_id"]
            order.executor_id = order_new["executor_id"]
            db.session.add(user)
            db.session.commit()
            return 'новые данные о заказе записаны'


    @app.route('/offers', methods=['POST', 'GET'])
    def all_offers():
        if request.method == 'GET':
            result = []
            for i in Offer.query.all():
                result.append(i.to_dict())
            return jsonify(result)
        elif request.method == 'POST':
            offer_raw = json.loads(request.data)
            offer = Offer(order_id=offer_raw["order_id"],
                          executor_id=offer_raw["executor_id"])
            db.session.add(offer)
            db.session.commit()
            return "предложение записано"


    @app.route('/offers/<x>', methods=['PUT', 'DELETE', 'GET'])
    def one_offer(x):
        if request.method == 'GET':
            return jsonify(Offer.query.get(x).to_dict())
        elif request.method == 'DELETE':
            offer = Offer.query.get(x)
            db.session.delete(offer)
            db.session.commit()
            return 'предложение удалено'
        elif request.method == 'PUT':
            offer_new = json.loads(request.data)
            offer = Offer.query.get(x)
            offer.id = offer_new['id']
            offer.order_id = offer_new["order_id"]
            offer.executor_id = offer_new["executor_id"]
            db.session.add(offer)
            db.session.commit()
            return 'новые данные о предложении записаны'


    app.run()
