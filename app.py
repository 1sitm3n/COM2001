from flask import Flask, request, jsonify
import pyodbc
import os

app = Flask(__name__)

# Database connection configuration
DB_SERVER = os.getenv("DB_SERVER")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Establish database connection
def get_db_connection():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD}"
    )
    return conn

@app.route('/addTrail', methods=['POST'])
def add_trail():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO CW2.Trail (Name, Description, LengthKm, OwnerID, AccessTypeID, TerrainTypeID, DifficultyID)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        data['name'], data['description'], data['lengthKm'], data['ownerID'],
        data['accessTypeID'], data['terrainTypeID'], data['difficultyID']
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Trail added successfully'}), 201

@app.route('/getTrails', methods=['GET'])
def get_trails():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CW2.Trail")
    rows = cursor.fetchall()
    trails = [{'TrailID': row[0], 'Name': row[1], 'Description': row[2], 'LengthKm': row[3]} for row in rows]
    conn.close()
    return jsonify(trails)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
