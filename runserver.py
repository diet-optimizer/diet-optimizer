from diet_optimizer import app
import os

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if __name__ == '__main__':
    # app.run(threaded=True, debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(threaded=True, debug=True, host='0.0.0.0', port=port)