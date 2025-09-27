
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


jackson_family = FamilyStructure("Jackson")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member is None:
            return jsonify({"error": "Member not found"}), 404
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route('/members', methods=['POST'])
def add_member():
    try:
       
        request_data = request.get_json()
        
       
        if request_data is None:
            return jsonify({"error": "No data provided"}), 400
        
        
        required_fields = ["first_name", "age", "lucky_numbers"]
        for field in required_fields:
            if field not in request_data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
       
        if not isinstance(request_data["first_name"], str):
            return jsonify({"error": "first_name must be a string"}), 400
        
        if not isinstance(request_data["age"], int) or request_data["age"] <= 0:
            return jsonify({"error": "age must be a positive integer"}), 400
        
        if not isinstance(request_data["lucky_numbers"], list):
            return jsonify({"error": "lucky_numbers must be a list"}), 400
        
        
        new_member = {
            "first_name": request_data["first_name"],
            "age": request_data["age"],
            "lucky_numbers": request_data["lucky_numbers"],
            "last_name": "Jackson"
        }
        
        
        if "id" in request_data and request_data["id"] is not None:
            new_member["id"] = request_data["id"]
        
        
        added_member = jackson_family.add_member(new_member)
        
        return jsonify(added_member), 200
        
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        deleted_member = jackson_family.delete_member(member_id)
        
        if deleted_member is None:
            return jsonify({"error": "Member not found"}), 404
        
        return jsonify({"done": True}), 200
        
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)