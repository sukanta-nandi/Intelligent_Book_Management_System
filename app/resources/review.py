from quart import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.future import select
from sqlalchemy import func
from app.database import async_session
from app.models import Review, Book
from app.schemas import ReviewSchema, BookSchema
from app.auth import token_required

review_bp = Blueprint('reviews', __name__)
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
book_schema = BookSchema()

@review_bp.route('/books/<int:book_id>/reviews', methods=['POST'], endpoint='create_review')
@token_required
async def create_review(current_user, book_id):
    try:
        review_data = await request.get_json()
        review_data['user_id'] = current_user.id  # Set user_id to current user
        review_data['book_id'] = book_id  # Ensure book_id is included in the review data
        review = review_schema.load(review_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    async with async_session() as session:
        # Check if the book exists
        result = await session.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if not book:
            return jsonify({'message': 'Book not found'}), 404

        session.add(Review(**review))
        await session.commit()
        return jsonify(review_schema.dump(review)), 201

@review_bp.route('/books/<int:book_id>/reviews', methods=['GET'], endpoint='get_reviews_for_book')
@token_required
async def get_reviews_for_book(current_user, book_id):
    async with async_session() as session:
        result = await session.execute(select(Review).where(Review.book_id == book_id))
        reviews = result.scalars().all()
        return jsonify(reviews_schema.dump(reviews))

@review_bp.route('/books/<int:book_id>/summary', methods=['GET'], endpoint='get_book_summary')
@token_required
async def get_book_summary(current_user, book_id):
    async with async_session() as session:
        result = await session.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if not book:
            return jsonify({'message': 'Book not found'}), 404

        # Get the summary and aggregated rating
        result = await session.execute(select(
            func.count(Review.id).label('review_count'),
            func.avg(Review.rating).label('average_rating')
        ).where(Review.book_id == book_id))
        summary = result.fetchone()

        book_summary = {
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'year_published': book.year_published,
            'summary': book.summary,
            'review_count': summary.review_count,
            'average_rating': summary.average_rating
        }
        return jsonify(book_summary)
