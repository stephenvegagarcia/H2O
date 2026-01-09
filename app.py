"""
Flask Web Application for Satellite Water Shield System
Provides real-time visualization of system data and metrics.
"""

from flask import Flask, render_template, jsonify
from water_shield import (
    SatelliteWaterShield,
    WaterShieldConfig,
    OrbitalParameters
)

app = Flask(__name__)

# Initialize the water shield system
water_shield = SatelliteWaterShield()


@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')


@app.route('/api/status')
def get_status():
    """API endpoint to get current system status."""
    status = water_shield.get_system_status(exposure_days=7)
    return jsonify(status)


@app.route('/api/status/<int:days>')
def get_status_for_days(days):
    """API endpoint to get system status for specific exposure duration."""
    status = water_shield.get_system_status(exposure_days=days)
    return jsonify(status)


@app.route('/api/update_config', methods=['POST'])
def update_config():
    """API endpoint to update system configuration (future enhancement)."""
    # Placeholder for dynamic configuration updates
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🛰️  SATELLITE WATER SHIELD SYSTEM - WEB INTERFACE")
    print("="*70)
    print("\n🌐 Starting Flask server...")
    print("📊 Dashboard will be available at: http://127.0.0.1:5000")
    print("\n💡 Press Ctrl+C to stop the server\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000)
