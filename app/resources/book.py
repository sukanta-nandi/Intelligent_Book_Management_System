from quart import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.future import select
from app.database import async_session
from app.models import Book
from app.schemas import BookSchema
from app.auth import token_required

book_bp = Blueprint('books', __name__)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

@book_bp.route('/books/<int:id>', methods=['GET'], endpoint='get_book')
@token_required
async def get_book(current_user, id):
    async with async_session() as session:
        result = await session.execute(select(Book).where(Book.id == id))
        book = result.scalar_one_or_none()
        if book:
            return jsonify(book_schema.dump(book))
        return jsonify({'message': 'Book not found'}), 404

@book_bp.route('/books', methods=['POST'], endpoint='create_book')
@token_required
async def create_book(current_user):
    try:
        book_data = await request.get_json()
        book = book_schema.load(book_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    async with async_session() as session:
        session.add(Book(**book))
        await session.commit()
        return jsonify(book_schema.dump(book)), 201

@book_bp.route('/books/<int:id>', methods=['PUT'], endpoint='update_book')
@token_required
async def update_book(current_user, id):
    try:
        book_data = await request.get_json()
        updated_book_data = book_schema.load(book_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    async with async_session() as session:
        result = await session.execute(select(Book).where(Book.id == id))
        book = result.scalar_one_or_none()
        if book:
            for key, value in updated_book_data.items():
                setattr(book, key, value)
            await session.commit()
            return jsonify(book_schema.dump(book))
        return jsonify({'message': 'Book not found'}), 404

@book_bp.route('/books/<int:id>', methods=['DELETE'], endpoint='delete_book')
@token_required
async def delete_book(current_user, id):
    async with async_session() as session:
        result = await session.execute(select(Book).where(Book.id == id))
        book = result.scalar_one_or_none()
        if book:
            await session.delete(book)
            await session.commit()
            return jsonify({'message': 'Book deleted'})
        return jsonify({'message': 'Book not found'}), 404

@book_bp.route('/books', methods=['GET'], endpoint='get_books')
@token_required
async def get_books(current_user):
    async with async_session() as session:
        result = await session.execute(select(Book))
        books = result.scalars().all()
        return jsonify(books_schema.dump(books))
