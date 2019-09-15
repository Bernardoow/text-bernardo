import os

import nltk
nltk.download('punkt')

from app import create_app


# if __name__ == "__main__":

if "HEROKU" in os.environ:
    app = create_app("heroku.cfg")
elif "TESTING" in os.environ:
    app = create_app("test.cfg")
else:
    app = create_app("dev.cfg")
