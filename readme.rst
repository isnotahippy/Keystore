KeyStore
========
KeyStore is a simple app that is the product of a weekend hack. 
A place to store simple strings/text and associate it with a key. 

I find myself with an unhealthy amount of stickies containing useful snippets of information,
in a completly unrealiable and unsearchable environment. KeyStore is intended to replace this.

Work in progress
----------------
I am still implementing the front end and intend to add a simple search function.

Testing
-------

cd keystore
coverage run ../manage.py test --settings=keystore.settings.test