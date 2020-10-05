import face_recognition
import cv2, os, mysql.connector
import numpy as np
from tkinter.messagebox import *
import tkinter.ttk as ttk
from tkinter import *
class HotelAutomation:
    def __init__(self):
        self.container = Tk()
        self.container.title("Hotel Automation Management System")
        self.mainFrame = Frame(self.container, bg="yellow")
        self.total_amount = 0
        self.cascPath = "cascades\\data\\haarcascade_frontalface_default.xml"
        self.mainPage()
        self.container.mainloop()

    def mainPage(self):
        self.labelFrame = Frame(self.container, bg="yellow")
        self.labelFrame.pack(side="left", expand=YES, fill=BOTH)
        self.labelFrame.grid_propagate(0)
        Label(self.labelFrame, text=".............", bg="yellow").pack(pady=7)
        Label(self.labelFrame, text="Full Name:", bg="yellow").pack(pady=7)
        Label(self.labelFrame, text="Phone:", bg="yellow").pack(pady=10)
        Label(self.labelFrame, text="passport:", bg="yellow").pack()

        self.entryFrame = Frame(self.container, bg="yellow", )
        self.entryFrame.pack(side="left", expand=YES, fill=BOTH)
        self.entryFrame.grid_propagate(0)
        Label(self.entryFrame, text="Registration Form", bg="yellow", font=('arial', 15, 'bold')).pack(side="top")
        self.fName = Entry(self.entryFrame, text="", width=14, font=('arial', 20))
        self.fName.pack()
        self.phone = Entry(self.entryFrame, text="", width=14, font=('arial', 20))
        self.phone.pack()
        self.passval = StringVar()
        self.passport = Entry(self.entryFrame, text=self.passval, width=14, font=('arial', 20))
        self.passport.pack()
        Button(self.entryFrame, text='Take passport', width=15, command=self.takePassport).pack(pady=5, padx=5)
        Button(self.entryFrame, text='Submit', width=15, command=self.submitForm).pack(padx=5)

        self.exitFrame = Frame(self.container, bg="brown")
        self.exitFrame.pack(side="left", expand=YES, fill=BOTH, padx=5)
        self.exitFrame.grid_propagate(0)
        Label(self.exitFrame, text="Exiting Hotel", bg="brown", font=('arial', 10, 'bold')).pack(side="top")
        Label(self.exitFrame, text="Full Name", bg="brown").pack(pady=7)
        self.exName = Entry(self.exitFrame, text="", width=14, font=('arial', 20))
        self.exName.pack()
        Button(self.exitFrame, text='Exit Hotel', width=15, command=self.total_spent).pack(pady=5, padx=5)
        self.visitArea()

    def visitArea(self):
        self.mainFrame.destroy()
        self.mainFrame = Frame(self.container, bg='green')
        self.mainFrame.pack(side="left", expand=YES, fill=BOTH)
        self.mainFrame.grid_propagate(0)
        self.visitFrame = Frame(self.mainFrame, bg='green')
        self.visitFrame.pack(side="left", expand=YES, fill=BOTH)
        self.visitFrame.grid_propagate(0)
        Label(self.visitFrame, text="Select Visiting Location", bg='green', font=('arial', 10, 'bold')).pack(side="top")
        Button(self.visitFrame, text='Bar Arena', width=15, command=lambda: self.number_of_people('Bar Arena', 2500)).pack(pady=5, padx=5)
        Button(self.visitFrame, text='Restaurant', width=15, command=lambda: self.number_of_people('Restaurant', 1500)).pack(pady=5, padx=5)
        Button(self.visitFrame, text='Swimming Pool', width=15, command=lambda: self.number_of_people('Swimming Pool', 2000)).pack(pady=5, padx=5)
        Button(self.visitFrame, text='Zoo Garden', width=15,  command=lambda: self.number_of_people('Zoo Garden', 1000)).pack(pady=5, padx=5)

        self.amountFrame = Frame(self.mainFrame, bg="green")
        self.amountFrame.pack(side="left", expand=YES, fill=BOTH, padx=5)
        self.amountFrame.grid_propagate(0)
        Label(self.amountFrame, text="Amount", bg="green", font=('arial', 10, 'bold')).pack(side="top")
        Label(self.amountFrame, text="#2500", bg="green").pack(pady=7)
        Label(self.amountFrame, text="#1500", bg="green").pack(pady=7)
        Label(self.amountFrame, text="#2000", bg="green").pack(pady=10)
        Label(self.amountFrame, text="#1000", bg="green").pack()

    def takePassport(self):
        faceCascade = cv2.CascadeClassifier(self.cascPath)
        video_capture = cv2.VideoCapture(0)
        while (True):
            # Capture frame-by-frame
            ret, frame = video_capture.read()
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Display the resulting frame
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                ret, frame = video_capture.read()
                cv2.imshow("Captured", frame)
                cv2.imwrite(filename="knownImage\\"+self.fName.get()+".jpg", img=frame)
                self.passval.set(os.path.join(os.path.dirname(os.path.abspath("knownimage")),self.fName.get()+".jpg"))
                cv2.waitKey(1650)
                break
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
        # When everything done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()

    def submitForm(self):
        mycon = mysql.connector.connect(host='localhost', user='root', passwd='', database='hotelautomation')
        mycursor = mycon.cursor()
        myquery = "INSERT INTO registration (Full_Name, Phone, Passport) VALUES(%s, %s, %s)"
        val = (self.fName.get(), self.phone.get(), self.passport.get())
        mycursor.execute(myquery, val)
        mycon.commit()
        showinfo("Successful", "Registration Failed")
        mycon.close()

    def number_of_people(self, visit, amt):
        self.amt =amt
        self.visit = visit
        self.mainFrame.destroy()
        self.mainFrame = Frame(self.container, bg='green')
        self.mainFrame.pack(side="left", expand=YES, fill=BOTH)
        self.mainFrame.grid_propagate(0)
        self.visitFrame = Frame(self.mainFrame, bg='green')
        self.visitFrame.pack(side="left", expand=YES, fill=BOTH)
        self.visitFrame.grid_propagate(0)
        self.peopleFrame = Frame(self.visitFrame, bg='green')
        self.peopleFrame.pack(side="left", expand=YES, fill=BOTH)
        self.peopleFrame.grid_propagate(0)
        Label(self.peopleFrame, text="Select Visiting Location", bg='green', font=('arial', 10, 'bold')).pack(side="top")
        item = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
        self.cob = ttk.Combobox(self.peopleFrame, values=(item))
        self.cob.set("0")
        self.cob.pack()
        Button(self.peopleFrame, text='Visit', width=15, command=lambda: self.identifyImage(self.visit, self.amt)).pack(pady=5, padx=5)
        Button(self.peopleFrame, text='Back', width=15, command=self.visitArea).pack(pady=5, padx=5)

    def identifyImage(self, visit, amount):
        self.known_face_names = []
        self.known_face_image = []
        self.known_face_encodings = []
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(BASE_DIR, "knownImage")
        for root, dirs, files in os.walk(image_dir):
            for file in files:
                if file.endswith("png") or file.endswith("jpg"):
                    path = os.path.join(root, file)
                    # Create arrays of known face encodings and their names
                    self.known_face_names.append(os.path.basename(path).split(".")[0])
                    self.known_face_image.append(path)

        # Get a reference to webcam #0 (the default one)
        video_capture = cv2.VideoCapture(0)
        # Load a sample picture and learn how to recognize it.
        for face_image in self.known_face_image:
            _image = face_recognition.load_image_file(face_image)
            # Create arrays of known face encodings and their names
            self.known_face_encodings.append(face_recognition.face_encodings(_image)[0])

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        name = ""
        process_this_frame = True
        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                    face_names.append(name)
            process_this_frame = not process_this_frame
            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            # Display the resulting image
            cv2.imshow('Video', frame)
            # Compare identified number of faces with number of registered people allowed to visit
            if np.array(face_encodings).shape[0] > int(self.cob.get()) or np.array(face_encodings).shape[0] == 0:
                print("You are more than the number of registered people.\n Please remove others or add them up")
                self.enter = False
            else:
                self.enter = True
                print("You are welcome, proceed in as we wish you a nice time")
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
        if self.enter:
            number_alowed = int(self.cob.get())
            mycon = mysql.connector.connect(host='localhost', user='root', passwd='', database='hotelautomation')
            mycursor = mycon.cursor()
            myquery = "INSERT INTO locations (Full_Name, Visited, Number_of_people, Amount) VALUES(%s, %s, %s, %s)"
            val = (name, visit, int(self.cob.get()), (amount*number_alowed))
            mycursor.execute(myquery, val)
            mycon.commit()

    def total_spent(self):
        total_amount = 0.0
        mycon = mysql.connector.connect(host='localhost', user='root', passwd='', database='hotelautomation')
        mycursor = mycon.cursor()
        myquery = "SELECT *  FROM locations WHERE Full_Name = %s"
        mycursor.execute(myquery, (self.exName.get(),))
        for value in mycursor.fetchall():
            total_amount += value[3]
        myquery = "UPDATE registration SET Amount = %s WHERE Full_Name = %s"
        val = (total_amount, self.exName.get())
        mycursor.execute(myquery, val)
        mycon.commit()
        mycon.close()
        showinfo("Receipt", "Your total amount spent is "+str(total_amount)+".\n Thanks for coming hope to see you again.")

if __name__ == "__main__":
    HotelAutomation()