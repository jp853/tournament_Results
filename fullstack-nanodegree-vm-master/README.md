Udacity Full Stack Nanodegree
Tournament Results Project

Project Specifications

You will develop a database schema to store the game matches between players. You will then write code to query this data and determine the winners of various games.

-- Files

- tournament.py -- Runs Swiss-system tournament
- tournament.sql -- Table definitions required for the tournament project.
- tournament_test.py -- Test cases for tournament.py

How to run tournament

A Vagrantfile has been provided that will setup postgresql and create the tournament schema

    - Install vagrant "https://www.vagrantup.com/downloads.html"
    - CD to the vagrant file and startup vagrant: vagrant up
    - Login to the vagrant VM: vagrant ssh
    - Move to the tournament folder: cd /vagrant/tournament
    - Create the schema: psql -f tournament.sql
    - Run the program: python tournament_test.py
