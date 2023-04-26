from App import HOST, PORT
from App.Routes.main import MainApp
from uvicorn import run


if __name__ == "__main__":
    run(MainApp, host=HOST, port=PORT, )
