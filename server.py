from flask import Flask, jsonify, request
from paho.mqtt import publish

web_client = Flask(__name__)
@web_client.route("/<topic>", methods=["POST"])
def index(topic):
 jreq = request.json
 publish.single(topic=topic, payload=jreq["payload"])
 return jsonify({"message":"sent"})

web_client.run(port=8282)