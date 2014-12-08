
import sys
from random import randint
from getpass import getpass
import smtplib


class NaughtyElf:
	'''Represents a member of a secret santa trade'''	
	#the person who this person has to buy for
	sending_email = None
	sending_pass = None

	def __init__(self):
		self.selected_person = None
		self.first_name = None
		self.last_name = None
		self.email = None
	
	def getName(self):
		return self.first_name + " " + self.last_name

	def write(self):
		next_name = "(null)"
		if self.selected_person:
			next_name = self.selected_person.getName()
		print "Naughty Elf: " + self.getName() + " - " + self.email + " : (Next ->) " + next_name + "\n"

	#sends an email to this person saying that they have to buy for the other person
	def sendEmail(self):
		if self.selected_person:
			#send an email saying that you have this person from our secret santa email!
			content = '''Your secret santa person is {0}! Buy them a present, but don't spend more than 15 bucks. Sorry for annoying you with emails. Luv, J'''
			return send_gmail(self.email, content.format(self.selected_person.getName()))
		else:
			return False


def send_gmail(target_email, content):
            
            gmail_user = NaughtyElf.sending_email
            gmail_pwd = NaughtyElf.sending_pass
            FROM = NaughtyElf.sending_email
            TO = [target_email] #must be a list
            SUBJECT = "Welcome to Secret Santa! (use this one)"
            TEXT = content

            # Prepare actual message
            message = content
            try:
                #server = smtplib.SMTP(SERVER) 
                server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message)
                #server.quit()
                server.close()
                return True
            except:
            	#try to debug the error...
            	print "Error (" + target_email + "): ", sys.exc_info()[0]
                return False


def main():

	#prompt for email information
	sending_email = raw_input("Email: ")
	sending_pass = getpass()

	#set the class variables so that we can access these things later
	NaughtyElf.sending_email = sending_email
	NaughtyElf.sending_pass = sending_pass

	#initialize by prompting for file of secret santas
	secret_santas_file = raw_input("File of participant information: ")

	#validate the input file
	participants = loadParticipantsFromFile(secret_santas_file)

	if not participants:
		print "Couldn't load participants. Exiting...\n"
		return

	yes_no = raw_input("Commence drawings? Participants will be emailed. (y/n): ")
	if (yes_no in ["Y", "y"]):
		commenceDrawings(participants)
		return 0
	else:
		print "Exiting..."
		return 1




def commenceDrawings(participants):
	if len(participants) == 1:
		print "Invalid scenario. You need more than one person for secret santa, douche.\n"
		return False
	real_parts = list()
	
	#randomly pick one person to be the head
	head_index = randint(0,len(participants)-1)
	head = participants[head_index]
	del participants[head_index]
	real_parts.append(head)
	last = head
	next = None


	#precondition - last is never in the list. 
	while len(participants) > 0:
		next_index = randint(0,len(participants)-1)
		#pick a random person, and link them to the last. then swap...
		next = participants[next_index]
		last.selected_person = next
		print last.getName() + " -> " + next.getName()
		del participants[next_index]
		last = next
		real_parts.append(last)
		
	#finally, whoever was last, make them point to the head. circular list!!!! head is already in our final list.
	last.selected_person = head

	if verifyParticipants(real_parts):
		print "Drawings succeeded! Everybody is cool.\n"
		print "Proceeding...\n"
		for p in real_parts:
			if not p.sendEmail():
				print "Sending email failed to " + p.getName() + " \n" 
		print "People have been alerted... All done!"
		return True
	else:
		print "Drawings failed. Seriously, get a better programmer.\n"
		return False


def verifyParticipants(part):
	print "Validity of results of drawing....\n"

	print "Current State: \n"
	for p in part:
		p.write()


	head = part[0]
	#since this is a circular linked list, we should end up at the head...
	seen = list()
	seen.append(head)
	
	cur = head.selected_person
	while (cur and (not cur in seen)):
		seen.append(cur)
		cur = cur.selected_person
	if len(seen) == len(part):
		print "We did it!\n"
		return True
	else:
		return False

def loadParticipantsFromFile(filename):
	#open the file
	participants = list()

	f = open(filename, "r")
	if not f:
		return participants
	line_no = 1
	for line in f:
		#iterate through the lines of the file
		parts = line.split()
		if len(parts) == 3:
			newFriend = NaughtyElf()
			newFriend.first_name = parts[0]
			newFriend.last_name = parts[1]
			newFriend.email = parts[2]
			participants.append(newFriend)
		else:
			print "Invalid format. Got " + str(len(parts)) + " elements on line #" + str(line_no) + ", but expected 3.\n"
			return None
		line_no = line_no + 1
	return participants



main()