from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=128, default='')
    description = models.TextField(max_length=512, default='')
    count = models.IntegerField(default=10)
    authors = models.ManyToManyField('author.Author')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Book(id={self.id})"

    @staticmethod
    def get_by_id(book_id):
        try:
            return Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(book_id):
        try:
            book = Book.objects.get(pk=book_id)
            book.delete()
            return True
        except Book.DoesNotExist:
            return False

    @staticmethod
    def create(name, description, count=10, authors=None):
        if len(name) > 128:
            return None
        book = Book.objects.create(name=name, description=description, count=count)
        if authors:
            book.authors.set(authors)
        return book

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'authors': [author.to_dict() for author in self.authors.all()],
        }

    def update(self, name=None, description=None, count=None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if count is not None:
            self.count = count
        self.save()

    def add_authors(self, authors):
        if authors:
            self.authors.add(*authors)
            self.save()

    def remove_authors(self, authors):
        if authors:
            self.authors.remove(*authors)
            self.save()

    @staticmethod
    def get_all():
        return Book.objects.all()
