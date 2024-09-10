# app.py
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL 데이터베이스 연결 설정
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # MySQL 사용자 이름
        password='gpdus0405',  # MySQL 비밀번호
        database='Service'  # 데이터베이스 이름
    )
    return connection

@app.route('/api/vehicle-data', methods=['POST'])
def receive_vehicle_data():
    data = request.json
    vehicle_id = data.get('vehicle_id')

    if not vehicle_id:
        return jsonify({'status': 'error', 'message': 'Vehicle id is required'}), 400
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO vehicles (vehicle_id) VALUES (%s)"
        cursor.execute(query, (vehicle_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'status': 'success'}), 200
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
