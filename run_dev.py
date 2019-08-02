from orders import create_app
from orders.config import DevelopmentConfig

if __name__ == '__main__':

    app = create_app(DevelopmentConfig)
    app.run()
