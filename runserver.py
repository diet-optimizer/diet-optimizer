<<<<<<< HEAD
from diet_optimizer import app
import os

app.secret_key = "development-key"
if __name__ == '__main__':
    # app.run(threaded=True, debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(threaded=True, debug=True, host='0.0.0.0', port=port)
=======
from diet_optimizer import app
import os

if __name__ == '__main__':
    # app.run(threaded=True, debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(threaded=True, debug=True, host='0.0.0.0', port=port)
>>>>>>> 3d29df7e1e9b3a0c9a7fb3c374995aedfbb1c424
