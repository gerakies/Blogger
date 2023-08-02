import os				# used in clear and rename
import time				# used in strftime and sleep
import textwrap			# used to wrap tex to fit screen
import datetime			# used to get today and birthdate
import nltk.tokenize	# used to retain day and date info on edit
import glob2			# v1.32 used to retieve filename list
import password			# v1.50 validate user against file userlist.csv
import zipfile			# v1.54 used to create a zip file

VERSION="1.54" 			# Update this on every iteration.
						# v1.2 preserves the day and date portion of the
						#		post on edit
						# v1.3 introduces a logging module that logs all
						#		changes. Access is hidden keyword is log
						# 		also changed the hidden access to the 
						#		documention from h to help
						# v1.31 start and end of session logged
						# v1.32 changed filename retieval from os.listdir() to glob2
						# v1.33 added additional function screen "more" to activate
						# v1.34 added a merge all blogs to one text file funtion.
						# v1.35 Added the ability to read all archined posts
						# v1.36 changed all to merge
						# v1.40 Option added to archive all files after merging
						# v1.41 increased menu size
						# v1.42 added the uarc function to recover archived posts
						# v1.43 tidied up the comments
						# v1.50 Added a security logon security module.
						# v1.51 Included password encryption module
						# v1.52 corrected some bad grammar on the more screen
						# v1.53 corrected a sequence bug in the rename_files routine
						# v1.54 Added the ability to archive to zip an entire year and
						#		optionally delete the files.
						#		Also added a module to display file stats.
						
	# Function to create a new blog post.
def create_post():
	today = datetime.date.today()			#used to calculate days and delta
	month_name = today.strftime("%B")		#used in opening post
	day = today.strftime("%d")				#used in opening post
	birth_date = datetime.date(1956, 2, 10) #author's birthdate
	delta = today - birth_date				#number of days since birthdate
	title = time.strftime("%Y%m%d-%H%M%S") 	#file name based on creation time
	print(f"Today is Day {delta.days}. {month_name} {day}")
	content = input("Enter content of the blog post: ")
	if content == "":
		print("Null return - request aborted.")
		time.sleep(2)
		return
	post = f"Day {delta.days}. {month_name} {day}. {content}"
	with open(f"{title}.blg", "w") as f: 	#.blg = blog file
		f.write(post)
	write_log(title+".blg", "New Post    ", post)
	print(title+" created.")
	time.sleep(2)

	# Sub function check for yes/no response
def check_yesno(question):
	yn="x"
	while yn !="y" and yn !="n":
		yn=input(question)
		if yn=="y":
			answer=True
		if yn=="n":
			answer=False
	return answer	

	# Sub function to preserve 1st 2 sentences when editing
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

	#Sub function to archive posts
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
	print("Archive of all blogs complete")
	time.sleep(3)
	
	#Sub function to display banner
def display_header():
	global VERSION
	os.system('clear')
	print()
	print("          ╔══════════════════════════════════════╗")
	print("          ║ Quick and Dirty Blogger Version "+VERSION+" ║")
	print("          ║                                      ║")
	print("          ║            Current Entries           ║")
	print("          ║                                      ║")
	print("          ╚══════════════════════════════════════╝")
	print()
	
	# Sub function to get a list of all files and sort them in descending order
def sort_posts(suffix):
	display_header()
	files = glob2.glob(suffix)
	files.sort()
	return(files)
    
    # Sub Function to display the content of each file.
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

	# Function to archive a year to a zip file.
def create_zip():
	zip_year = input("Enter year to archive. ")
	zip_name = "All_"+zip_year+"_posts.zip"
	zip_year = zip_year+"*.*"
	files_to_zip = count_files(zip_year)
	if files_to_zip == 0:
		print("There are no files in that year.")
		time.sleep(3)
		return
	else:
		proceed = check_yesno("Proceed to archive "+str(files_to_zip)+" posts?")
		if proceed:
			with zipfile.ZipFile(zip_name, 'w') as zipf:
				file_paths = glob2.glob(os.path.join('',zip_year))
				for file_path in file_paths:
					# Calculate the relative path of each file
					relative_path = os.path.relpath(file_path, '')
					zipf.write(file_path, relative_path)
					write_log(file_path,"archived to ",zip_name)
			print(f"{zip_name} created with {files_to_zip} posts.")
			delete_files = check_yesno("Delete original posts now?")
			if delete_files:
				for file_path in file_paths:
					os.remove(file_path)
					write_log(file_path,"deleted","")
				print(f"{files_to_zip} posts deleted.")
				time.sleep(3)
			else:
				print("Original posts left intact.")
				time.sleep(3)

	# Sub function to count files based on a supplied mask
def count_files(file_mask):
	file_list = glob2.glob(file_mask)
	file_count = len(file_list)
	return file_count
	
	# Function to display file statistics
def statistics():
	global VERSION
	file_types = [
		['*.blg', 'Blogger  Posts'],
		['*.blx', 'Deleted  Posts'],
		['*.arc', 'Archived Posts'],
		['*.doc', 'Documentation '],
		['*.txt', 'Text files    '],
		['*.csv', 'CSV Files     '],
		['*.zip', 'Zip files     '],
		['*.log', 'Log files     '],
		['*.py', 'Program files ']
	]
	os.system('clear')
	print()
	print("          ╔══════════════════════════════════════╗")
	print("          ║ Quick and Dirty Blogger Version "+VERSION+" ║")
	print("          ║                                      ║")
	print("          ║           File Statistics            ║")
	print("          ║                                      ║")
	total_files = len(glob2.glob('*.*'))
	files_counted = 0
	for row in file_types:
		spacer=""
		file_list = glob2.glob(row[0])
		file_count = len(file_list)
		files_counted += file_count
		if file_count < 10:
			spacer = " "
		print(f"          ║           {row[1]} = {file_count}        {spacer}║")
	if total_files-files_counted < 10: 
		spacer=" "
	else:
		spacer=""
	print(f"          ║           Other files    = {total_files-files_counted}        {spacer}║")
	print("          ║                                      ║")
	print("          ╚══════════════════════════════════════╝")
	print()
	write_log("                   ","            ","Statistics viewed.")
	input("Press Enter to continue...")	

	# Function to display the log file
def view_log():
	write_log("                   ","            ","Log viewed.")
	with open("Blogger.log", "r") as f:
		content = f.read()
		print(content)
	print()
	input("Press Enter to continue...")	

	# Function to edit a selected post.
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

	# Sub function to display the content of each file.
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

	# Function to delete a selected post
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

	# Function to recover a selected post
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
	
	# Function to append a selected post.			
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

	# Sub function to write to log file V1.30
def write_log(filename, action, text):
	date_time = time.strftime("%Y%m%d-%H%M%S")
	with open('Blogger.log', "a") as f:
		log_entry = (f"{date_time} - {filename} - {action} - {text}")
		f.write(f"{log_entry}\n")

	# Function to merge all blogs to one file for onward editing and 
	#	optionally to archive them.
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
		print("          ╔══════════════════════════════════════╗")
		print("          ║ Quick and Dirty Blogger Version "+VERSION+" ║")
		print("          ║                                      ║")
		print("          ║           [n] New     Post           ║")
		print("          ║           [l] List    Posts          ║")
		print("          ║           [e] Edit    Post           ║")
		print("          ║           [a] Append  Post           ║")
		print("          ║           [d] Delete  Post           ║")
		print("          ║           [r] Recover Post           ║")
		print("          ║                                      ║")
		print("          ║           more                       ║")
		print("          ║                                      ║")
		print("          ║                                      ║")
		print("          ║           [q] Quit                   ║")
		print("          ║                                      ║")
		print("          ╚══════════════════════════════════════╝")
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
		elif choice == "zip":
			create_zip()
		elif choice == "stat":
			statistics()
		elif choice == "uarc":
			recover_posts("*.arc")
		elif choice == "q":
			break
		else:
			print("Invalid choice. Please try again.")
			time.sleep(2)

	# Sub function to additional menu items
def additional_functions():
	global VERSION
	os.system('clear')
	print()
	print("          ╔══════════════════════════════════════╗")
	print("          ║ Quick and Dirty Blogger Version "+VERSION+" ║")
	print("          ║                                      ║")
	print("          ║        Additional commands           ║")
	print("          ║                                      ║")
	print("          ║        arc  - read all archives      ║")
	print("          ║        help - system documentation   ║")
	print("          ║        log  - displays log file      ║")
	print("          ║        merge- merges all blogs into  ║")
	print("          ║               one file All_Blogs.txt ║")
	print("          ║               and archives posts     ║")
	print("          ║        more - this screen            ║")
	print("          ║        stat - file statistics        ║")
	print("          ║        uarc - recover an archive     ║")
	print("          ║        zip  - zip a whole year       ║")
	print("          ║                                      ║")
	print("          ╚══════════════════════════════════════╝")
	print()
	input("Press Enter to return...")
	write_log("                   ","            ","more screen viewed")	

	# Runtime
#valid_user, admin_flag = password.validate_user()
valid_user=True
if valid_user:
	write_log("                   ","            ","Session start.")
	main()
	write_log("                   ","            ","Session stop.")
else:
	print(f"                 Invalid user/password combination. Program terminated.")
	time.sleep(5)
	os.system('clear')
