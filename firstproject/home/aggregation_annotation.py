import os
import sys
import django
from django.db.models import Count, Avg, Sum, Min, Max

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firstproject.settings')

django.setup()

from home.models import Book, Author


def countBooks():
    books_count = Book.objects.count()
    print(f'Number of books: {books_count}' if books_count == 1 else f'Number of books: {books_count}')

countBooks()

def averagePrice():
    average_price = Book.objects.aggregate(Avg('price'))
    print(f'Average price: {average_price["price__avg"]:.2f}' if average_price else average_price)

averagePrice()

def totalPrice():
    total_price = Book.objects.aggregate(Sum('price'))
    print(f'Total price: {total_price["price__sum"]:.2f}' if total_price else total_price)

totalPrice()

def minPrice():
    min_price = Book.objects.aggregate(Min('price'))
    print(f'Minimum price: {min_price["price__min"]:.2f}' if min_price else min_price)

minPrice()

def maxPrice():
    max_price = Book.objects.aggregate(Max('price'))
    print(f'Maximum price: {max_price["price__max"]:.2f}' if max_price else max_price)

maxPrice()

def countBooksByAuthor():
    books_by_author = Author.objects.annotate(book_count=Count('book'))#.values('name', 'book_count')
    for author in books_by_author:
        print(f'Author: {author.author_name}, Number of books: {author.book_count}')

countBooksByAuthor()

def totalAndAveragePriceByAuthor():
    price_stats_by_author = Author.objects.annotate(total_price=Sum('book__price'),
                                                    average_price=Avg('book__price'))
    for author in price_stats_by_author:
        if author.total_price is not None and author.average_price is not None:
        # print(type(author.total_price), type(author.average_price))
            print(f'Author: {author.author_name}, Total Price: {author.total_price:.2f}, Average Price: {author.average_price:.2f}')

totalAndAveragePriceByAuthor()

def booksPublishedAfterYear(year):
    books_in_year = Book.objects.filter(published_date__year__gte=year).filter(price__gte= 50)
    print(f'Books published in {year}:')
    for book in books_in_year:
        print(f'- {book.book_name} by {book.author.author_name}')

booksPublishedAfterYear(2015)



# Subquery Example
from django.db.models import OuterRef, Subquery, Q

def latestBookByAuthor():
    # This is a subquery which will only run as part of a main query.
    latest_books = Book.objects.filter(author=OuterRef('pk')).order_by('-published_date')
    # This is the main query which will use the subquery to annotate each author with the name of their latest book.
    authors_with_latest_book = Author.objects.annotate(latest_book_name=Subquery(latest_books.values('book_name')[:1]))
    for author in authors_with_latest_book:
        print(f'Author: {author.author_name}, Latest Book: {author.latest_book_name}')

latestBookByAuthor()

def totalPriceofBooksPublishedByEachAuthorInYear(year):
    total_price_by_author = Author.objects.annotate(total_price=Sum('book__price',
                                                                    filter=Q(book__published_date__year__gte=year))).filter(total_price__isnull=False)
    for author in total_price_by_author:
        print(f'Author: {author.author_name}, Total Price of Books Published in {year}: {author.total_price:.2f}' if author.total_price else f'Author: {author.author_name}, Total Price of Books Published in {year}: 0.00')

totalPriceofBooksPublishedByEachAuthorInYear(2020)

def secondHighestPricedBookInYear(year):
    second_highest_price = Book.objects.filter(published_date__year=year).order_by('-price').values_list('price', flat=True).distinct()[1:2]
    second_highest_book = Book.objects.filter(price=second_highest_price).first()
    if second_highest_book:
        print(f'Second Highest Priced Book: {second_highest_book.book_name} by {second_highest_book.author.author_name} with price {second_highest_book.price:.2f}')
    else:
        print('No second highest priced book found.')

secondHighestPricedBookInYear(2020)



from django.db.models.functions import TruncMonth
def authorMonthWiseTotalPriceOfBooksPublishedInYear(year):

    data = (
        Book.objects
        .filter(published_date__year=year)
        .annotate(month=TruncMonth('published_date'))
        .values('author__author_name', 'month')
        .annotate(total_price=Sum('price'))
        .order_by('month')
    )

    for entry in data:
        month_str = entry['month'].strftime('%B %Y')
        print(f'Author: {entry["author__author_name"]}, Month: {month_str}, Total Price: {entry["total_price"]:.2f}')

authorMonthWiseTotalPriceOfBooksPublishedInYear(2020)