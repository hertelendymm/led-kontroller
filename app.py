from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

current_led_state = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/led/state', methods=['GET', 'PUT'])
def handle_led_state():
    global current_led_state
    if request.method == 'GET':
        print(f"[Szerver] Kliens lekérdezte az állapotot: {current_led_state}")
        return jsonify({'state': current_led_state})
    
    elif request.method == 'PUT':
        data = request.get_json()
        if 'state' in data and isinstance(data['state'], bool):
            new_state = data['state']
            if current_led_state != new_state:
                current_led_state = new_state
                print(f"[Szerver] Állapotváltozás PUT kéréssel: {current_led_state}. Mikrokontroller értesítése következik (logika helye)...")
                # ITT JÖNNE A LOGIKA, AMI ÉRTESÍTI A MIKROKONTROLLERT
            else:
                print(f"[Szerver] Állapot nem változott (már {current_led_state} volt).")
            return jsonify({'state': current_led_state, 'message': 'LED state updated on server.'})
        else:
            return jsonify({'error': 'Invalid data payload. "state" (boolean) is required.'}), 400

# Ez egy külön végpont lehet, amit a mikrokontroller használhat pollingra.
# Így az /api/led/state logikája egyszerűbb maradhat.
@app.route('/api/mcu/get_desired_state', methods=['GET'])
def mcu_get_desired_state():
    print(f"[Szerver] Mikrokontroller lekérdezte a kívánt állapotot: {current_led_state}")
    return jsonify({'state': current_led_state})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)