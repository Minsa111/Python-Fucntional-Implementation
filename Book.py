import tkinter as tk
from functools import reduce
from tkinter import simpledialog, messagebox

def lowercase_input_decorator(func):
    def wrapper(*args, **kwargs):
        ans = func(*args, **kwargs)
        return ans.lower() if ans else ans
    return wrapper


class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.currentUser = None

        self.users = {
            "admin": "12345",
            "user1": "1",
            "user2": "2"
        }

        self.users_book = {}
        self.user_role = {
            "admin": True,
            "user1": False,
            "user2": False
        }

        self.book = {
            "J.K Rowling": "Harry Potter",
            "Finn the Human": "Adventure Time"
        }

        self.title("Humble Library")

        self.login_frame()



    
    def login_frame(self):
        login_frame = tk.Frame(self)
        login_frame.configure(bg="#292929")
        login_frame.pack(padx=10, pady=10)
        
        tk.Label(login_frame, text="Username:", fg="white", bg="#292929").grid(row=0, column=0)
        tk.Label(login_frame, text="Password:", fg="white", bg="#292929").grid(row=1, column=0)

        username_entry = tk.Entry(login_frame)
        password_entry = tk.Entry(login_frame, show="*")

        username_entry.grid(row=0, column=1)
        password_entry.grid(row=1, column=1)

        login_button = tk.Button(login_frame, text="Login", command=lambda: self.login(username_entry.get(), password_entry.get()))
        login_button.grid(row=2, columnspan=2, pady=10)

    def admin_frame(self):
        admin_frame = tk.Frame(self)
        admin_frame.pack(padx=10, pady=10)

        tk.Label(admin_frame, text=f"Welcome {self.currentUser}!").grid(row=0, column=0, columnspan=2)

        options = ["Input Book", "Check Borrowed Book", "Check All Book", "Log Out"]
        buttons = []

        for i, option in enumerate(options, start=1):
            buttons.append(tk.Button(admin_frame, text=option, command=lambda opt=option: self.admin_options(opt)))
            buttons[-1].grid(row=i, columnspan=2, pady=5)

    def norm_user_frame(self):
        user_frame = tk.Frame(self)
        user_frame.pack(padx=10, pady=10)

        tk.Label(user_frame, text=f"Welcome {self.currentUser}!").grid(row=0, column=0, columnspan=2)

        options = ["Borrow Book", "Check Borrowed Book", "Return Book", "Log Out"]
        buttons = []

        for i, option in enumerate(options, start=1):
            buttons.append(tk.Button(user_frame, text=option, command=lambda opt=option: self.user_options(opt)))
            buttons[-1].grid(row=i, columnspan=2, pady=5)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def login(self, username, password):
        role = self.check_acc(username, password)

        if role == "admin":
            self.currentUser = username
            self.clear_frame()
            self.admin_frame()
        elif role == "user":
            self.currentUser = username
            self.clear_frame()
            self.norm_user_frame()
        else:
            messagebox.showinfo("Login Failed", "Wrong username or password.")

    def check_acc(self, username, password):
        if username in self.users and self.user_role[username] and password == self.users[username]:
            return "admin"
        elif username in self.users and not self.user_role[username] and password == self.users[username]:
            return "user"
        else:
            return "Wrong username or Password"

    def admin_options(self, option):
        if option == "Input Book":
            self.add_book()
        elif option == "Check Borrowed Book":
            self.check_borrowed_book(self.users_book)
        elif option == "Check All Book":
            self.check_data(self.book)
        elif option == "Log Out":
            self.currentUser = None
            self.clear_frame()
            self.login_frame()

    def user_options(self, option):
        if option == "Borrow Book":
            self.borrow_book()
        elif option == "Check Borrowed Book":
            self.borrowed_book()
        elif option == "Return Book":
            self.return_book()
        elif option == "Log Out":
            self.currentUser = None
            self.clear_frame()
            self.login_frame()

    def add_book(self):
        author = simpledialog.askstring("Input author name", "Author:")
        title = simpledialog.askstring("Input title name", "Title:")

        if author and title:
            self.book[author] = title
            messagebox.showinfo("Success", "Successfully added a book!")
            messagebox.showinfo("Books", self.show_books(self.book))
        else:
            messagebox.showinfo("Error", "Author and title cannot be empty.")

    def check_borrowed_book(self, user_book):
        messagebox.showinfo("Borrowed Books", self.show_books(user_book))

    def check_data(self, available_books):
        messagebox.showinfo("Available Books", self.show_books(available_books))
        
    @lowercase_input_decorator
    def get_user_input(self, title, prompt):
        return simpledialog.askstring(title, prompt)
    
    def borrow_book(self):
        messagebox.showinfo("Books available for borrowing", self.show_books(self.book))

        ans = self.get_user_input("Borrow Book", "Enter the book title to borrow:")

        found_book = list(filter(lambda item: item[1].lower() == ans, self.book.items()))

        if found_book:
            found_book = found_book[0]
            already_borrowed = list(filter(lambda item: item[0] == found_book, self.users_book.items()))
            if already_borrowed:
                messagebox.showinfo("Error", f"Book already borrowed by {already_borrowed[0][1]}")
            else:
                self.users_book[found_book] = self.currentUser
                self.borrowed_book()
        else:
            messagebox.showinfo("Error", "Book not found.")

    def borrowed_book(self):
        messagebox.showinfo("Borrowed Books", self.show_borrowed_books(self.currentUser, self.users_book))

    def return_book(self):
        messagebox.showinfo("Books borrowed by", f"{self.currentUser}:\n{self.show_borrowed_books(self.currentUser, self.users_book)}")

        book_to_return = simpledialog.askstring("Return Book", "Enter the book title to return:")

        book_found = list(filter(lambda item: item[1] == book_to_return, self.users_book.items()))

        if book_found:
            book_found = book_found[0][0]
            del self.users_book[book_found]
            messagebox.showinfo("Success", f"You've returned the book: {book_found[0]} : {book_found[1]}")
        else:
            messagebox.showinfo("Error", "You don't have a book with that title.")

    def show_books(self, books):
        def print_book(item):
            return f"{item[0]}: {item[1]}"

        book_list = list(map(print_book, books.items()))
        return '\n'.join(book_list)

    def show_borrowed_books(self, user, user_book):
        borrowed_books = list(filter(lambda item: item[1] == user, user_book.items()))

        if borrowed_books:
            titles = [item[0][1] for item in borrowed_books]
            concatenated_titles = reduce(lambda acc, title: acc + ", " + title, titles)
            return f"{user} has borrowed the following books: {concatenated_titles}"
        else:
            return f"{user} has not borrowed any books."

if __name__ == "__main__":
    app = LibraryApp()
    app.configure(bg="#292929")
    app.mainloop()
