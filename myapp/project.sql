CREATE DATABASE stock;
USE stock;

CREATE TABLE products (
    productid int PRIMARY KEY auto_increment,
    productname text not null,
    quantity int,
    price int,
    status text
);

CREATE TABLE customer (
    customerid int PRIMARY KEY auto_increment ,
    customername text not null,
    phonenumber text
);

CREATE TABLE orders (
    orderid SERIAL PRIMARY KEY,
    customerid INT,
    productid INT,
    quantity INT,
    amount float,
    created_at timestamp default current_timestamp);
    
create table admin(
 adminid serial primary key,
 adminname text not null,
 emailid text not null,
 password text not null);
 
select * from products;
select * from customer;
select * from orders;
select * from admin;