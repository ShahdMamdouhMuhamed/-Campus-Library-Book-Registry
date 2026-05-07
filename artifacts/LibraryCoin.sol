// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LibraryCoin {

    string public name = "Library Coin";
    string public symbol = "LBRC";
    uint8 public decimals = 18;
    uint public totalSupply;

    address private admin;

    mapping(address => uint) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint value);

    modifier onlyOwner() {
        require(msg.sender == admin, "Not admin");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    function mint(address to, uint amount) public onlyOwner {
        require(to != address(0), "Invalid address");
        balanceOf[to] += amount;
        totalSupply += amount;
        emit Transfer(address(0), to, amount);
    }

    function transfer(address to, uint amount) public returns (bool) {
        require(to != address(0), "Invalid address");
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        emit Transfer(msg.sender, to, amount);
        return true;
    }
}