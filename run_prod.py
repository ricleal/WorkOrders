from orders import create_app
from orders.config import ProductionConfig
app = create_app(ProductionConfig)

if __name__ == '__main__':
    app.run()
