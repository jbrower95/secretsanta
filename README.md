secretsanta
===========

Secret Santa - A python script for managing a secret santa group / gift exchange!


Usage:

Make a file with three columns, whitespace seperated, as follows:
...
FIRST LAST EMAIL
...

Include no extra blank lines. 

Once you have this file, quickly set up a gmail account for the group to receive messages from. Alternatively, use one of your own gmail addresses.

Run the script using

    python secretsanta.py
    
The script will prompt you for a username / password for the gmail account. This script is only configured for gmail accounts!

After prompting for gmail information, it will prompt you for the location of the three-columned file we made previously.
Now, to make sure you actually want to go through with it, type "y" to confirm. 

After this, you'll see some lines detailing who has who in the gift exchange. You should get a bunch of success messages, or a failure if your gmail account details are incorrect.




TODO: 
  - implement support for other email address types
  - implement adding late people / removing people from the gift exchange
  - implement some sort of 'state' system, so that you can recall a past gift exchange and make changes.
  - clean up code
