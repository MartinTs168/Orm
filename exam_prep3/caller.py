import os
import django
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article


# Create queries within functions

def get_authors(search_name=None, search_email=None):
    if search_email and search_name:
        query = Q(full_name__icontains=search_name) & Q(email__icontains=search_email)
    elif search_email:
        query = Q(email__icontains=search_email)
    elif search_name:
        query = Q(full_name__icontains=search_name)
    else:
        return ""

    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors:
        return ""

    result = []
    for author in authors:
        result.append(f"Author: {author.full_name}, email: {author.email}, status: "
                      f"{'Banned' if author.is_banned else 'Not Banned'}")

    return '\n'.join(result)


def get_top_publisher():
    top_author = Author.objects.get_authors_by_article_count().first()

    if top_author is None or top_author.article_count == 0:
        return ""

    return f"Top Author: {top_author.full_name} with {top_author.article_count} published articles."


def get_top_reviewer():
    top_reviewer = (
        Author.objects
        .prefetch_related('reviews')
        .annotate(review_count=Count('reviews'))
        .filter(review_count__gt=0)
        .order_by('-review_count', 'email')
        .first()
    )

    if not top_reviewer:
        return ""

    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.review_count} published reviews."


def get_latest_article():
    article = (
        Article.objects
        .prefetch_related('authors', 'reviews')
        .order_by('-published_on')
        .first()
    )
    if not article:
        return ""

    authors_names = ', '.join(a.full_name for a in article.authors.order_by('full_name') if a)
    reviews_count = article.reviews.count()
    avg_article_rating = sum([r.rating for r in article.reviews.all()]) / reviews_count if reviews_count else 0

    return (f"The latest article is: {article.title}. Authors: {authors_names}. "
            f"Reviewed: {reviews_count} times. "
            f"Average Rating: {avg_article_rating:.2f}.")


def get_top_rated_article():
    article = (
        Article.objects
        .prefetch_related('reviews')
        .annotate(rating_avg=Avg('reviews__rating'))
        .order_by('-rating_avg', 'title')
        .first()
    )

    if not article or article.reviews.count() == 0:
        return ""

    return (f"The top-rated article is: {article.title}, "
            f"with an average rating of {article.rating_avg:.2f}, reviewed {article.reviews.count()} times.")


def ban_author(email=None):
    if email is None:
        return "No authors banned."

    author = Author.objects.filter(email=email).first()

    if not author:
        return "No authors banned."

    author.is_banned = True
    author_reviews_count = author.reviews.count()
    author.reviews.all().delete()
    author.save()

    return f"Author: {author.full_name} is banned! {author_reviews_count} reviews deleted."


