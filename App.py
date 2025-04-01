from flask import Flask, request, jsonify

app = Flask(__name__)

file_path = "data.csv"

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json["payload"]

    ax, ay, az = data["accelerometer"]
    gx, gy, gz = data["gyroscope"]

    content = [ax, ay, az, gx, gy, gz]

    with open(file_path, "a") as file:
        file.write(",".join(str(x) for x in content) + "\n")

    print(data)
    return jsonify({"response": "yay"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")