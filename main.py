import os  # accessing the os functions
import check_camera
import Capture_Image
import Train_Image
import Recognize


# creating the title bar function

def title_bar():
    os.system('cls')  # for windows

    # title of the program

    print("\t")
    print("\t Face Recognition In Surveilance System ")
    print("\t")


# creating the user main menu function

def mainMenu():
    title_bar()
    print()
    print(10 * "*", "MENU", 10 * "*")
    print("[1] Check Camera")
    print("[2] Capture Faces")
    print("[3] Train Images")
    print("[4] Recognize face")
    print("[5] Quit")

    while True:
        try:
            choice = int(input("Enter Choice: "))

            if choice == 1:
                checkCamera()
                break
            elif choice == 2:
                CaptureFaces()
                break
            elif choice == 3:
                Trainimages()
                break
            elif choice == 4:
                RecognizeFaces()
                break
            elif choice == 5:
                print("Thank You")
                break
            else:
                print("Invalid Choice. Enter 1-4")
                mainMenu()
        except ValueError:
            print("Invalid Choice. Enter 1-4\n Try Again")
    exit


def checkCamera():
    check_camera.camer()
    key = input("Enter any key to return main menu")
    mainMenu()


def CaptureFaces():
    Capture_Image.takeImages()
    key = input("Enter any key to return main menu")
    mainMenu()

def Trainimages():
    print('in1')
    Train_Image.TrainImages()
    key = input("Enter any key to return main menu")
    mainMenu()

def RecognizeFaces():
    Id=Recognize.recognize_face()
    print(Id)
    key = input("Enter any key to return main menu")
    mainMenu()

mainMenu()