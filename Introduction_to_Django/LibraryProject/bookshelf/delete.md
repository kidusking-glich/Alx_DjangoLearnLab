deleted_count, _ = retrieved_book.delete()
Book.objects.all()

# Expected Output (Confirming 1 book deleted and an empty queryset)
(1, {'bookshelf.Book': 1})
<QuerySet []>