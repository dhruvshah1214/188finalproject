import os
from source.web import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    print("STARTING SERVER")
    app.run(debug=True, host='0.0.0.0', port=port)