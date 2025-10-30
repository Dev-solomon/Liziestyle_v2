from main import create_app
import os
# import logging



if __name__ == "__main__":
  app = create_app()
  PORT = int(os.environ.get('PORT', app.config["FLASK_PORT"]))
  HOST = os.environ.get('HOST', app.config["FLASK_DOMAIN"])
  
  
  app.run(debug=True, host=HOST, port=PORT)
# else:
#   app = create_app()
#   logging.basicConfig(app.config["FLASK_DIRECTORY"] + "trace.log", level=logging.DEBUG)
