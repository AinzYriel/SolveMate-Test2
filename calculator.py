@calc_bp.route('/explain', methods=['POST'])
def explain_calculation():
    """DEBUG VERSION - Forces explanation response."""
    try:
        data = request.json
        print("🧪 DEBUG /api/explain RECEIVED:", data)  # SERVER LOG
        
        # FORCE SIMPLE RESPONSE for testing
        return jsonify({
            'res': 19.6,
            'unit': 'm/s',
            'explanation': [
                "🧠 Test Formula: v = u + at",
                "📖 u = 0 m/s, a = 9.8 m/s², t = 2 s", 
                "🔢 v = 0 + 9.8 × 2 = 19.6 m/s",
                "✅ Final Answer: 19.6 m/s"
            ]
        })
        
    except Exception as e:
        print("🧪 DEBUG ERROR:", str(e))  # SERVER LOG
        return jsonify({'error': f'Debug error: {str(e)}'}), 500
