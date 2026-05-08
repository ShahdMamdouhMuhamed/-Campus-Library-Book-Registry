// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Library {

    // ================= ADMIN =================
    address private admin;

    modifier onlyOwner() {
        require(msg.sender == admin, "Not admin");
        _;
    }

    function getAdmin() public view returns(address) {
        return admin;
    }

    // ================= PAUSE =================
    bool public paused = false;

    modifier whenNotPaused() {
        require(!paused, "System paused");
        _;
    }

    event Paused();
    event Resumed();

    function pause() public onlyOwner {
        paused = true;
        emit Paused();
    }

    function resume() public onlyOwner {
        paused = false;
        emit Resumed();
    }

    // ================= BOOK =================
    struct Book {
        string title;
        bool available;
        address borrower;
    }

    mapping(uint => Book) public books;
    uint public totalBooks;

    modifier bookExists(uint id) {
        require(bytes(books[id].title).length > 0, "Book not found");
        _;
    }

    // ================= USERS =================
    mapping(address => string) public users;

    function registerUser(string memory name) public {
        require(bytes(users[msg.sender]).length == 0, "Already registered");
        users[msg.sender] = name;
    }

    // ================= EVENTS =================
    event BookAdded(uint id, string title);
    event BookBorrowed(address user, uint bookId);
    event BookReturned(address user, uint bookId);
    event OwnershipTransferred(address oldAdmin, address newAdmin);

    // ================= CONSTRUCTOR =================
    constructor() {
        admin = msg.sender;
    }

    // ================= ADD BOOK =================
    function addBook(uint id, string memory title) public onlyOwner {
        require(bytes(books[id].title).length == 0, "Book exists");

        books[id] = Book(title, true, address(0));
        totalBooks++;

        emit BookAdded(id, title);
    }

    // ================= BATCH ADD =================
    function batchAddBooks(uint[] memory ids, string[] memory titles) public onlyOwner {
        require(ids.length == titles.length, "Mismatch");

        for (uint i = 0; i < ids.length; i++) {
            require(bytes(titles[i]).length > 0, "Invalid title");
            require(bytes(books[ids[i]].title).length == 0, "Book exists");

            books[ids[i]] = Book(titles[i], true, address(0));
            totalBooks++;

            emit BookAdded(ids[i], titles[i]);
        }
    }

    // ================= BATCH UPDATE =================
    function batchUpdateAvailability(uint[] memory ids, bool[] memory status) public onlyOwner {
        require(ids.length == status.length, "Mismatch");

        for (uint i = 0; i < ids.length; i++) {
            require(bytes(books[ids[i]].title).length > 0, "Book not found");
            books[ids[i]].available = status[i];
        }
    }

    // ================= BORROW =================
    function borrowBook(uint id) public whenNotPaused bookExists(id) {
        Book storage book = books[id];

        require(bytes(users[msg.sender]).length > 0, "Register first");
        require(book.available, "Not available");

        book.available = false;
        book.borrower = msg.sender;

        emit BookBorrowed(msg.sender, id);
    }

    // ================= RETURN =================
    function returnBook(uint id) public whenNotPaused bookExists(id) {
        Book storage book = books[id];

        require(book.borrower == msg.sender, "Not your book");

        book.available = true;
        book.borrower = address(0);

        emit BookReturned(msg.sender, id);
    }

    // ================= OWNERSHIP =================
    function transferOwnership(address newAdmin) public onlyOwner {
        require(newAdmin != address(0), "Invalid address");

        address old = admin;
        admin = newAdmin;

        emit OwnershipTransferred(old, newAdmin);
    }
}