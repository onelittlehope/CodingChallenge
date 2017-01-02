# Run a test server
from mynextbus import app

if __name__ == '__main__':
    # WARNING!
    # Do not set threaded=True or processes=n where n > 1 as the query stats gathering code is not thread safe.
    app.run(host='0.0.0.0', port=8081, debug=False, threaded=False)
