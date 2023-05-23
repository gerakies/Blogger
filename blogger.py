import os
import time
import textwrap
import datetime
import nltk.tokenize	#used to retain day and date info on edit
import glob2			# v1.32 used to retieve filename list

VERSION="1.40" 			# Update this on every iteration.
						# v1.2 preserves the day and date portion of the post
						# on edit.
						# v1.3 introduces a logging module that logs all changes
						# hidden access will be log
						# also changed the hidden access to the documention from h to help
						# v1.31 start and end of session logged
						# v1.32 changed filename retieval from os.listdir() to glob2
						# v1.33 added additional function screen "more" to activate
						# v1.34 added a merge all blogs to one text file funtion.
						# v1.35 Added the ability to read all archined posts
						# v1.36 changed all to merge
						# v1.40 Option added to archive all files after merging
						
	# Function to create a new blog post.
def create_post():
	today = datetime.date.today()		#used to calculate days and delta
	month_name = today.strftime("%B")	#used in opening post
	day = today.strftime("%d")			#used in opening post
	birth_date = datetime.date(1956, 2, 10) #author's birthdate
	delta = today - birth_date			#number of days since birthdate
	title = time.strftime("%Y%m%d-%H%M%S") #file name based on creation time
	print(f"Today is Day {delta.days}. {month_name} {day}")
	content = input("Enter content of the blog post: ")
	if content == "":
		print("Null return - request aborted.")
		time.sleep(2)
		return
	post = f"Day {delta.days}. {month_name} {day}. {content}"
	with open(f"{title}.blg", "w") as f: #.blg = blog file
		f.write(post)
	write_log(title+".blg", "New Post    ", post)
	print(title+" created.")
	time.sleep(2)

#check for yes/no response
def check_yesno(question):
	yn="x"
	while yn !="y" and yn !="n":
		yn=input(question)
		if yn=="y":
			answer=True
		if yn=="n":
			answer=False
	return answer	


def keep_headers(filename):
	headers=""
	preserve=check_yesno("CAUTION - Preserve Headers? (y/n):")
	if preserve:
		# Load the file
		with open(filename, 'r') as file:
			text = file.read()
		# Tokenize the text into sentences
		sentences = nltk.sent_tokenize(text)
		# Extract the first two sentences
		headers = ' '.join(sentences[:2])
	return(headers)

def rename_files(old_suffix, new_suffix):
	# Get the list of files in the directory
	files = os.listdir()
	for file_name in files:
		# Check if the file ends with the old suffix
		if file_name.endswith(old_suffix):
			# Construct the new file name by replacing the old suffix with the new suffix
			new_name = file_name[:-len(old_suffix)] + new_suffix

			# Rename the file
			old_file = file_name
			new_file = new_name
			os.rename(old_file, new_file)
			write_log(old_file, "Archived to ", new_file)
			print(f"Archived {file_name} to {new_name}")
			time.sleep(1)
			print("Archive of all blogs complete")

       
def display_header():
	global VERSION
	os.system('clear')
	print()
	print("          ╔═════════════════════════════════════╗")
	print("          ║Quick and Dirty Blogger Version "+VERSION+" ║")
	print("          ║                                     ║")
	print("          ║           Current Entries           ║")
	print("          ║                                     ║")
	print("          ╚═════════════════════════════════════╝")
	print()
	
	# Get a list of all files and sort them in descending order
def sort_posts(suffix):
	display_header()
	#files = [f for f in os.listdir() if f.endswith(suffix)]
	files = glob2.glob(suffix)
	files.sort()
	return(files)
    
    # Display the content of each file.
def view_posts(suffix):
	if suffix == "*.blg":
		file_type="Posts"
	elif suffix == "*.doc":
		file_type="Documention"
	elif suffix == "*.txt":
		file_type="Text files"
	elif suffix == "*.arc":
		file_type="Archives"

	for file in sort_posts(suffix):
		with open(file, "r") as f:
			raw_post = f.read()
			wrapped_post = textwrap.wrap(raw_post, width=80)
			for line in wrapped_post:
				print(line)
		print()
	write_log("                   ","            ",(file_type+" viewed."))
	input("Press Enter to continue...")	
	
	

def view_log():
	write_log("                   ","            ","Log viewed.")
	with open("Blogger.log", "r") as f:
		content = f.read()
		print(content)
	print()
	input("Press Enter to continue...")	
		

	# Edit a selected post.
def edit_posts(suffix):
	post_num, files=post_option(suffix)
	if post_num==0:
		return
	headers=keep_headers(files[int(post_num)-1])
	with open(files[int(post_num)-1], "r+") as f:
		content = f.read()
		f.seek(0)
		f.truncate()
		display_header()
		print(f"\n{content}\n")
		write_log(files[int(post_num)-1], "Edit from   ", content)
		new_content = input("Enter new content to the post: ")
		f.write(f"{f.readline().strip()}{headers} {new_content}")
		write_log(files[int(post_num)-1], "Edit to     ", f"{headers} {new_content}")
		print("Post updated.")
		time.sleep(2)

	# Display the content of each file.
def post_option(suffix):
	files=sort_posts(suffix)
	for i, file in enumerate(files):
		with open(file, "r") as f:
			print(f"{i+1}. {f.readline()}")
		print()
		    
    # Get the number of the post to append or edit.
	while True:
		post_num = input("Enter the number of the post (or null to quit): ")
		if post_num == "":
			post_num=0
			print("Null return - request aborted.")
			time.sleep(2)
			return(post_num, files)
		elif not post_num.isnumeric():
			print("Invalid input. Please try again.")
		elif int(post_num) < 1 or int(post_num) > len(files):
			print("Invalid post number. Please try again.")
		else:
			return(post_num, files)

	# Delete a selected post
def delete_posts(suffix):
	post_num, files=post_option(suffix)
	if post_num==0:
		return
	filename=files[int(post_num)-1]
	with open(files[int(post_num)-1], "r") as f:
		content = f.read()
	base_name, extension = os.path.splitext(filename)
	new_filename = base_name + ".blx"  
	os.rename(filename, new_filename)
	write_log(filename, "Delete Post ", content)
	print("Blog "+base_name+" has been deleted")
	time.sleep(2)

	# Recover a selected post
def recover_posts(suffix):
	post_num, files=post_option(suffix)
	if post_num==0:
		return
	filename=files[int(post_num)-1]
	with open(files[int(post_num)-1], "r") as f:
		content = f.read()
	base_name, extension = os.path.splitext(filename)
	new_filename = base_name + ".blg"  
	os.rename(filename, new_filename)
	write_log(filename, "Recover Post", content)
	print("Blog "+base_name+" has been recovered")
	time.sleep(2)

	
	# Append a selected post.			
def append_posts(suffix):
	post_num, files=post_option(suffix)
	if post_num==0:
		return    
	with open(files[int(post_num)-1], "r") as f:
		content = f.read()
		display_header()
		print(f"\n{content}\n")
	with open(files[int(post_num)-1], "a") as f:
		new_content = input("Append new content to the post: ")
		f.write(f" {new_content}")
		write_log(files[int(post_num)-1], "Append Post ", new_content)
		print("Post updated.")
		time.sleep(2)

	# Write to log file V1.30
def write_log(filename, action, text):
	date_time = time.strftime("%Y%m%d-%H%M%S")
	with open('Blogger.log', "a") as f:
		log_entry = (f"{date_time} - {filename} - {action} - {text}")
		f.write(f"{log_entry}\n")

	# Merge all blogs to one file for onward editing
def merge_all_blogs(suffix):
	text_files = glob2.glob(suffix)
	text_files.sort()
	# Concatenate the content of the text files
	concatenated_text = ""
	for text_file in text_files:
		with open(text_file, "r") as file:
			file_content = file.read()
			concatenated_text += file_content + "\n\n"  # Add a line break between files
	output_file = "All_Blogs.txt"
	# Write the concatenated text to the output file
	with open(output_file, "w") as o:
		o.write(concatenated_text)
	write_log((output_file+"      "),"Merge Blogs ","Created")
	print(f"All blogs merged to file {output_file}.")
	ok_to_archive=check_yesno("CAUTION - Archive all merged blogs? (y/n):")
	if ok_to_archive:
		rename_files(".blg",".arc")
	else:
		print("No blogs were archived.")
	time.sleep(4)
	
	
	# Main function to run the program.
def main():
	global VERSION
	while True:
		os.system('clear')
		print()
		print("          ╔═════════════════════════════════════╗")
		print("          ║Quick and Dirty Blogger Version "+VERSION+" ║")
		print("          ║                                     ║")
		print("          ║          [n] New     Post           ║")
		print("          ║          [l] List    Posts          ║")
		print("          ║          [e] Edit    Post           ║")
		print("          ║          [a] Append  Post           ║")
		print("          ║          [d] Delete  Post           ║")
		print("          ║          [r] Recover Post           ║")
		print("          ║                                     ║")
		print("          ║          [q] Quit                   ║")
		print("          ║                                     ║")
		print("          ╚═════════════════════════════════════╝")
		print()
		choice = input("Select: ")
		if choice == "n":
			create_post()
		elif choice == "l":
			view_posts("*.blg")
		elif choice == "e":
			edit_posts("*.blg")
		elif choice == "a":
			append_posts("*.blg")
		elif choice == "d":
			delete_posts("*.blg")
		elif choice == "r":
			recover_posts("*.blx")
		elif choice == "help":
			view_posts("*.doc")
		elif choice == "log":
			view_log()
		elif choice == "more":
			additional_functions()
		elif choice == "merge":
			merge_all_blogs("*.blg")
		elif choice == "arc":
			view_posts("*.arc")
		elif choice == "q":
			break
		else:
			print("Invalid choice. Please try again.")
			time.sleep(2)

def additional_functions():
	global VERSION
	os.system('clear')
	print()
	print("          ╔═════════════════════════════════════╗")
	print("          ║Quick and Dirty Blogger Version "+VERSION+" ║")
	print("          ║                                     ║")
	print("          ║       Additional commands           ║")
	print("          ║                                     ║")
	print("          ║       arc  - read all archives      ║")
	print("          ║       help - system documentation   ║")
	print("          ║       log  - displays log file      ║")
	print("          ║       merge- merges all blogs into  ║")
	print("          ║              one file All_Blogs.txt ║")
	print("          ║       more - this screen            ║")
	print("          ║                                     ║")
	print("          ╚═════════════════════════════════════╝")
	print()
	input("Press Enter to return...")
	write_log("                   ","            ","more screen")	
            
write_log("                   ","            ","Session start.")
if __name__ == "__main__":
	main()
write_log("                   ","            ","Session stop.")
