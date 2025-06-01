from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Initialize lamps with 6 slots each (30% chance of being occupied)
lamps = [{
    'id': i,
    'device_id': f'BT-LAMP-{i:03d}',
    'slots': [random.random() < 0.3 for _ in range(6)],  # True = occupied
    'location': f'Zone {i//10 + 1}',
    'status': 'green'  # Will be updated immediately
} for i in range(1, 101)]

# Set initial status based on slots
for lamp in lamps:
    lamp['status'] = 'red' if all(lamp['slots']) else 'green'

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/lamps', methods=['GET'])
def get_lamps():
    return jsonify(lamps)

@app.route('/api/lamps/<int:lamp_id>', methods=['PUT'])
def update_lamp(lamp_id):
    lamp = next((l for l in lamps if l['id'] == lamp_id), None)
    if not lamp:
        return jsonify({'error': 'Lamp not found'}), 404
    
    # Manual override (for testing)
    if 'status' in request.json:
        lamp['status'] = request.json['status']
    return jsonify({'success': True})

@app.route('/api/lamps/bulk_update', methods=['POST'])
def bulk_update():
    lamp_ids = request.json.get('lamp_ids', [])
    status = request.json.get('status')
    
    for lamp in lamps:
        if lamp['id'] in lamp_ids:
            lamp['status'] = status
    return jsonify({'success': True, 'updated': len(lamp_ids)})

if __name__ == '__main__':
    app.run(debug=True)