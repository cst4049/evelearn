import os
from ms.app import app

if __name__ == '__main__':
    port = os.environ.get('HTTP_PORT')
    app.run(debug=True,host='0.0.0.0',
            port = int(port) if
                    port else 8001)
