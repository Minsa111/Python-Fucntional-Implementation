from functools import reduce

currentUser = None

users = {
    "admin": "12345",
    "user1": "1",
    "user2": "2"
}
users_book = {}
user_role = {
    "admin": True,
    "user1": False,
    "user2": False
}

book = {
    "J.K Rowling": "Harry Potter",
    "Finn the Human": "Adventure Time"
}


def addBook():
    author = input("Input author name: ")
    title = input("Input title name: ")
    book[author] = title
    print("Successfully added a book!")
    print(book)
    input("Press enter to continue...")


def checkBorrowedBook(userBook):
    print(userBook)


def checkData():
    print(book)
    input("Press enter to continue...")


def borrowBook():
    def printBook(item):
        print(f"{item[0]}: {item[1]}")

    print("Books available for borrowing:")
    list(map(printBook, book.items())) #it uses the function printBook

    ans = input("Enter the book title to borrow: ")

    found_book = list(filter(lambda item: item[1] == ans, book.items()))

    if found_book:
        found_book = found_book[0]
        already_borrowed = list(filter(lambda item: item[0] == found_book, users_book.items()))
        if already_borrowed:
            print("Book already borrowed by", already_borrowed[0][1])
        else:
            users_book[found_book] = currentUser
            borrowedBook()
    else:
        print("Book not found.")

    input("Press enter to continue...")


def borrowedBook():
    print(f"Books that are borrowed by {currentUser}:\n")
    borrowed_books = list(filter(lambda item: item[1] == currentUser, users_book.items()))

    if borrowed_books:
        # Extract titles from borrowed_books
        titles = [item[0][1] for item in borrowed_books]
        
        # Use reduce to concatenate titles into a single string
        concatenated_titles = reduce(lambda acc, title: acc + ", " + title, titles)
        
        print(f"{currentUser} has borrowed the following books: {concatenated_titles}")
    else:
        print(f"{currentUser} has not borrowed any books.")

    input("Press enter to continue")


def returnBook():
    print("Books borrowed by", currentUser + ":")
    borrowed_books = list(filter(lambda item: item[1] == currentUser, users_book.items()))
    list(map(lambda item: print(f"{item[0][0]} : {item[0][1]}"), borrowed_books))

    book_to_return = input("Enter the book title to return: ")

    book_found = list(filter(lambda item: item[1] == book_to_return, borrowed_books))

    if book_found:
        book_found = book_found[0][0]
        del users_book[book_found]
        print(f"You've returned the book: {book_found[0]} : {book_found[1]}")
    else:
        print("You don't have a book with that title.")

    input("Press enter to continue...")


def adminUser():
    global currentUser
    while True:
        print(f"Welcome {currentUser}!")
        print("1. Input Book")
        print("2. Check Borrowed Book")
        print("3. Check All Book")
        print("4. Log Out")
        ans = int(input("Please Choose one of the option: "))

        if ans == 1:
            addBook()
        elif ans == 2:
            checkBorrowedBook(users_book)
        elif ans == 3:
            checkData(users_book)
        elif ans == 4:
            currentUser = ""
            break  # Break out of the loop when logging out
        else:
            print("Please enter a valid answer")


def normUser():
    global currentUser
    while True:
        print(f"Welcome {currentUser}!")
        print("1. Borrow Book")
        print("2. Check Borrowed Book")
        print("3. Return Book")
        print("4. Log Out")
        ans = int(input("Please Choose one of the option: "))
        if ans == 1:
            borrowBook()
        elif ans == 2:
            borrowedBook()
        elif ans == 3:
            returnBook()
        elif ans == 4:
            currentUser = ""
            break  # Break out of the loop when logging out
        else:
            print("Please enter valid answer")


def login():
    global currentUser

    while True:
        print("\n--- Welcome to this Humble Library ---\n\n")
        username = input("Username: ")
        password = input("Password: ")
        role = checkAcc(username, password)

        if username and password:  # Check if both username and password are provided
            role = checkAcc(username, password)
            if role == "admin":
                currentUser = username
                adminUser()
            elif role == "user":
                currentUser = username
                normUser()
            else:
                print("Wrong username or password.")
        else:
            print("Please enter a valid username and password.")
            continue  # Continue prompting for login if credentials are not provided


def checkAcc(username, password):
    if username in users and user_role[username] and password == users[username]:
        return "admin"
    elif username in users and not user_role[username] and password == users[username]:
        return "user"
    else:
        return "Wrong username or Password"


def main():
    login()


if __name__ == "__main__":
    main()
