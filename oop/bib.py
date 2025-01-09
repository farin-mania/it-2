from datetime import datetime, timedelta
from enum import Enum
import json
from typing import List, Dict, Optional
import uuid


# Enum for ulike boktypar
class BookFormat(Enum):
    PHYSICAL = "physical"
    DIGITAL = "digital"
    AUDIO = "audio"


class Genre(Enum):
    FICTION = "fiction"
    NON_FICTION = "non_fiction"
    SCIENCE = "science"
    HISTORY = "history"
    FANTASY = "fantasy"
    MYSTERY = "mystery"


# Baseklasse for alle typar bøker
class Book:
    def __init__(
        self, title: str, authors: List[str], isbn: str, publish_year: int, genre: Genre
    ):
        self.id = str(uuid.uuid4())
        self.title = title
        self.authors = authors
        self.isbn = isbn
        self.publish_year = publish_year
        self.genre = genre
        self.times_borrowed = 0

    def get_format(self) -> BookFormat:
        raise NotImplementedError("Subclasses must implement get_format()")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "isbn": self.isbn,
            "publish_year": self.publish_year,
            "genre": self.genre.value,
            "format": self.get_format().value,
            "times_borrowed": self.times_borrowed,
        }


# Konkrete implementasjonar av ulike boktypar
class PhysicalBook(Book):
    def __init__(
        self,
        title: str,
        authors: List[str],
        isbn: str,
        publish_year: int,
        genre: Genre,
        shelf_location: str,
    ):
        super().__init__(title, authors, isbn, publish_year, genre)
        self.shelf_location = shelf_location

    def get_format(self) -> BookFormat:
        return BookFormat.PHYSICAL


class DigitalBook(Book):
    def __init__(
        self,
        title: str,
        authors: List[str],
        isbn: str,
        publish_year: int,
        genre: Genre,
        file_format: str,
    ):
        super().__init__(title, authors, isbn, publish_year, genre)
        self.file_format = file_format

    def get_format(self) -> BookFormat:
        return BookFormat.DIGITAL


class AudioBook(Book):
    def __init__(
        self,
        title: str,
        authors: List[str],
        isbn: str,
        publish_year: int,
        genre: Genre,
        duration_minutes: int,
    ):
        super().__init__(title, authors, isbn, publish_year, genre)
        self.duration_minutes = duration_minutes

    def get_format(self) -> BookFormat:
        return BookFormat.AUDIO


# Klasse for å handtere utlån
class Loan:
    def __init__(
        self, book_id: str, user_id: str, loan_date: datetime, due_date: datetime
    ):
        self.book_id = book_id
        self.user_id = user_id
        self.loan_date = loan_date
        self.due_date = due_date
        self.returned_date = None

    def is_overdue(self) -> bool:
        return not self.returned_date and datetime.now() > self.due_date

    def to_dict(self) -> dict:
        return {
            "book_id": self.book_id,
            "user_id": self.user_id,
            "loan_date": self.loan_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "returned_date": (
                self.returned_date.isoformat() if self.returned_date else None
            ),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Loan":
        loan = cls(
            book_id=data["book_id"],
            user_id=data["user_id"],
            loan_date=datetime.fromisoformat(data["loan_date"]),
            due_date=datetime.fromisoformat(data["due_date"]),
        )
        if data["returned_date"]:
            loan.returned_date = datetime.fromisoformat(data["returned_date"])
        return loan


class Library:
    def __init__(self, data_file: str = "library_data.json"):
        self.books: Dict[str, Book] = {}
        self.loans: List[Loan] = []
        self.data_file = data_file
        self.load_data()

    def add_book(self, book: Book) -> None:
        self.books[book.id] = book
        self.save_data()

    def get_available_copies(self, book_id: str) -> int:
        active_loans = sum(
            1
            for loan in self.loans
            if loan.book_id == book_id and not loan.returned_date
        )
        return max(0, 1 - active_loans)  # Antar 1 kopi per bok for enkelheits skuld

    def borrow_book(
        self, book_id: str, user_id: str, loan_duration_days: int = 14
    ) -> Optional[Loan]:
        if self.get_available_copies(book_id) == 0:
            return None

        loan = Loan(
            book_id=book_id,
            user_id=user_id,
            loan_date=datetime.now(),
            due_date=datetime.now() + timedelta(days=loan_duration_days),
        )
        self.loans.append(loan)
        self.books[book_id].times_borrowed += 1
        self.save_data()
        return loan

    def return_book(self, book_id: str, user_id: str) -> bool:
        for loan in self.loans:
            if (
                loan.book_id == book_id
                and loan.user_id == user_id
                and not loan.returned_date
            ):
                loan.returned_date = datetime.now()
                self.save_data()
                return True
        return False

    def get_overdue_loans(self) -> List[Loan]:
        return [loan for loan in self.loans if loan.is_overdue()]

    def get_popular_books(self, limit: int = 10) -> List[Book]:
        return sorted(
            self.books.values(), key=lambda x: x.times_borrowed, reverse=True
        )[:limit]

    def get_books_by_genre(self, genre: Genre) -> List[Book]:
        return [book for book in self.books.values() if book.genre == genre]

    def save_data(self) -> None:
        data = {
            "books": [book.to_dict() for book in self.books.values()],
            "loans": [loan.to_dict() for loan in self.loans],
        }
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_data(self) -> None:
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Gjenskape bøker
            for book_data in data["books"]:
                format_type = BookFormat(book_data["format"])

                if format_type == BookFormat.PHYSICAL:
                    book = PhysicalBook(
                        title=book_data["title"],
                        authors=book_data["authors"],
                        isbn=book_data["isbn"],
                        publish_year=book_data["publish_year"],
                        genre=Genre(book_data["genre"]),
                        shelf_location="A1",  # Default verdi
                    )
                elif format_type == BookFormat.DIGITAL:
                    book = DigitalBook(
                        title=book_data["title"],
                        authors=book_data["authors"],
                        isbn=book_data["isbn"],
                        publish_year=book_data["publish_year"],
                        genre=Genre(book_data["genre"]),
                        file_format="PDF",  # Default verdi
                    )
                else:  # AudioBook
                    book = AudioBook(
                        title=book_data["title"],
                        authors=book_data["authors"],
                        isbn=book_data["isbn"],
                        publish_year=book_data["publish_year"],
                        genre=Genre(book_data["genre"]),
                        duration_minutes=180,  # Default verdi
                    )
                book.id = book_data["id"]
                book.times_borrowed = book_data["times_borrowed"]
                self.books[book.id] = book

            # Gjenskape lån
            self.loans = [Loan.from_dict(loan_data) for loan_data in data["loans"]]

        except FileNotFoundError:
            # Ingen data å laste - startar med tomt bibliotek
            pass


def main():
    # Opprett bibliotek
    library = Library()

    # Legg til nokre bøker
    fantasy_book = PhysicalBook(
        title="The Hobbit",
        authors=["J.R.R. Tolkien"],
        isbn="978-0261103344",
        publish_year=1937,
        genre=Genre.FANTASY,
        shelf_location="F12",
    )

    digital_book = DigitalBook(
        title="Python Programming",
        authors=["John Smith"],
        isbn="978-1234567890",
        publish_year=2023,
        genre=Genre.NON_FICTION,
        file_format="PDF",
    )

    audio_book = AudioBook(
        title="The Great Gatsby",
        authors=["F. Scott Fitzgerald"],
        isbn="978-9876543210",
        publish_year=1925,
        genre=Genre.FICTION,
        duration_minutes=420,
    )

    # Legg til bøkene i biblioteket
    library.add_book(fantasy_book)
    library.add_book(digital_book)
    library.add_book(audio_book)

    # Test utlån
    loan = library.borrow_book(fantasy_book.id, "user123")
    if loan:
        print(f"Bok '{fantasy_book.title}' er lånt ut til {loan.due_date}")

    # Test innlevering
    library.return_book(fantasy_book.id, "user123")
    print(f"Bok '{fantasy_book.title}' er levert inn")

    # Vis populære bøker
    print("\nPopulære bøker:")
    for book in library.get_popular_books():
        print(f"{book.title}: Lånt ut {book.times_borrowed} gonger")

    # Vis forfalne lån
    print("\nForfalne lån:")
    for loan in library.get_overdue_loans():
        book = library.books[loan.book_id]
        print(f"Bok '{book.title}' skulle vore levert {loan.due_date}")


if __name__ == "__main__":
    main()
