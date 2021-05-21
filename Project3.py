################################################################################
### Engineering Computation: Project 3
### By Ellisa Booker
### My comments will be preceeded by "###". 
### Initial/your code comments are preceeded by '#'
################################################################################

# import the libraries needed to make all this work
import time
import os
from threading import Thread

# let the program know where you've put the data file
myDir = '/home/tug67203/ece_3822/ProjectCode'
filename = 'student_data.txt'

# create a class of type "student" that holds the data fields for each student.
# add whatever methods you see fit
class student:
    ###Initialize with a student, with name, ID, GPA, and time of packet arrival
    def __init__(self, fn = "", ln ="", i = 0, g = 0, m = "", t = 0.00):
        self.firstName = fn
        self.lastName = ln
        self.studentID = i
        self.GPA = g
        self.major = m
        self.timeOfArrival = t
        
    ###Allows us to print various forms of information about the student
    def printStudentInfo(self, x):
        if(x == "GPA"):
            print(self.GPA)
        if(x == "First name"):
            print(self.firstName)
        if(x == "Last name"):
            print(self.lastName)
        if(x == "ID"):
            print(self.studentID)
        if(x == "Major"):
            print(self.major)
        if(x == "TOA"):
            print(self.timeOfArrival)
        if(x == "All"):
            print("\n Student: " + self.firstName + " " + self.lastName + "\n ID: " + self.studentID + "\n GPA: " + self.GPA + "\n Major: " + self.major + "\n Packet Arrival: " + self.timeOfArrival)
           
    ###Allows us to return various forms of student information to outside functions
    def getStudentInfo(self, x):
        if(x == "GPA"):
           return self.GPA
        if(x == "First name"):
            return self.firstName
        if(x == "Last name"):
            return self.lastName
        if(x == "ID"):
            return self.studentID
        if(x == "Major"):
            return self.major
        if(x == "TOA"):
            return self.timeOfArrival

# this function will pop students out of the queue and place them in the hash
# table, which is to be a global variable called "hash_table"
def process_input_data(stop):
    global student_queue, hash_table
    
    ###Buffer length is hard-coded for now. When I tried to set it equal to len(student_queue), the code breaks
    ###I think this is possibly because the length of student queue updates every time a student is popped?
    ###I didn't want to mess with the structure of this function too much because I didn't understand it well enough, so this is my workaround
    buffLen = 40407
    
    ###Initialize the memory for a hash_table full of students with length of buffLen
    hash_table = [student] * buffLen

    while not stop() or len(student_queue)>0:
        if len(student_queue)>0 :
            
            
            ###First, pop the student from the queue
            s = student_queue.pop(0)
            
            ###Then get the student ID from this student
            studentID = int(s.getStudentInfo("ID"))
            
            ###I noticed that the first 5 digits of student ID numbers are typically different compared to the last 4
            ###So initially, I moduloed the studentID by 10000 to get the last 4 digits
            ###Then I subtracted from the studentID (studentID%buffLen = studentID if buffLen < studentID) to get the first 5 digits
            
            ###This worked for most ID searches, except ones where the first five digits were very similar
            ###AND/OR the result of (studentID%buffLen) - (studentID%10000) is very similar
            
            ###To add some more variation, I also subtracted the last digit of the studentID since that tends to vary between 1-7 (which is more variation than the 3 digits prior)
            key = ((studentID%buffLen) - (studentID%10000)) - (studentID%10)
            
            ###Now insert this student into the hash table at the index of the key
            ###I used the abs value function to account for any negatives that may come from my key equation
            hash_table[abs(key)] = s


###This function looks up a student in the hash table based on their student ID number  
def lookup_by_id(studentID, buffLen):
    ###To find the studentID in the hash table, we need to regenerate the key with the same equation in the previous function
    ###We also need to pass the buffLen to this function because we can't access it from the data processing function 
    key =((studentID%buffLen) - (studentID%10000)) - (studentID%10)
    
    ###Find the student at this index and print their information
    hash_table[abs(key)].printStudentInfo("All")
    
################################################################################
def main():

    global student_queue
    student_queue = []

    # set up the thread so that it can process students once they're in the queue.
    # do not modify this
    stop_threads = False
    thr = Thread(target=process_input_data,args =(lambda : stop_threads, ))
    thr.start()
    

    # load data from file, enforcing delays in order to simulate
    # asynchronous data arrivals
    os.chdir(myDir)
    
    ###This counter variable tracks the length of the student_queue so we can pass the buffer length to the lookup function
    buffLen = 0
    
    with open(filename,'r') as infile:
        # mark the initial time
        tStart = time.time()

        # for each line in the input file...
        for line in infile:

            # ... split the line into its components, and then ...        
            t, firstname, lastname, gpa, id_nmbr, mjr = line.split()
    
            # ... wait until the elapsed time matches the 'arrival' time of the
            #     line of data in the text file. This is how we are simulating
            #     data packets arriving at irregular times.
            while ((time.time()-tStart)< float(t) ):
                pass

            # when it's time, create a new object of type "student" and push
            # it onto the queue
            
            # YOUR CODE HERE
            # CREATE OBJECT USING  NAMES, GPA, ID, MAJOR, & PUSH IT TO student_queue
            
            ###Create a student object
            s = student(firstname, lastname, id_nmbr, gpa, mjr, t)
            ###Append it to the queue
            student_queue.append(s)
            ###Increment the buffer length counter
            buffLen = buffLen + 1


    # this is needed to stop the process_input_data function once all the data
    # has been read from the file into the queue
    stop_threads = True
    thr.join() 
    

    # add code to search the hash table for the students with these student IDs
    # and to print all their information
    ###     427980112
    ###     258399712
    ###     948140115
    # YOUR CODE HERE
    # FIND STUDENTS AND PRINT THEIR INFO
   
    studentID = 948140115
    lookup_by_id(studentID, buffLen)
    


if __name__=="__main__":
    main()