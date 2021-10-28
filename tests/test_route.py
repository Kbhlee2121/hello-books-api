# get all booksa nd return no records
def test_get_all_books_with_no_records(client):
    # Act
    response = client.get('/books')
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

# get one book by id
def test_get_book_by_id(client, two_saved_books):
    # Act
    response = client.get('/books/1')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr",
    }
