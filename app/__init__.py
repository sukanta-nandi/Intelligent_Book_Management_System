from quart import Quart
from app.config import Config
from app.database import init_db
from app.resources.book import book_bp
from app.resources.review import review_bp
from app.auth import auth_bp

app = Quart(__name__)
app.config.from_object(Config)

@app.before_serving
async def setup_db():
    await init_db()

# Register blueprints without a URL prefix
app.register_blueprint(book_bp)
app.register_blueprint(review_bp)
app.register_blueprint(auth_bp)
