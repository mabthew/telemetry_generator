import fileHandler
import processHandler
import datetime
import os
import pwd
import subprocess


def main():
    running = True

    printMenu()
    while running:
        userInput = input("command: ")
        running = executeCommand(userInput)


def printMenu():
    print(""" 
       ___ ____ _    ____ _  _ ____ ___ ____ _   _ 
        |  |___ |    |___ |\/| |___  |  |__/  \_/  
        |  |___ |___ |___ |  | |___  |  |  \   |   
                                                    
        ____ ____ _  _ ____ ____ ____ ___ ____ ____ 
        | __ |___ |\ | |___ |__/ |__|  |  |  | |__/ 
        |__] |___ | \| |___ |  \ |  |  |  |__| | \\
     """)

    print("\nGenerate and record endpoint activity.")

    print("\nOptions:")
    print("\t\'create [filename]\' \t\t Create a new file.")
    print("\t\'modify [filename] [content]\' \t Modify a file.")
    print("\t\'delete [filename]\' \t\t Delete a file.")
    print("\t\'run [command] [args...]\' \t Execute a command.")
    print("\t\'help\' \t\t\t Show this message.")
    print("\t\'exit\' \t\t\t Exit program.\n")


def parseInput(input):
    parsedInput = input.split(' ')

    return parsedInput[0], ' '.join(parsedInput[1:])


def executeCommand(userInput):
    action, args = parseInput(userInput)

    # get call info
    timestamp = datetime.datetime.now()
    username = pwd.getpwuid(os.getuid())[0]

    executor = None
    if action == "exit":
        return False
    elif action == "create":
        executor = fileHandler.FileHandler(timestamp, username)
        executor.create(args)
    elif action == "modify":
        executor = fileHandler.FileHandler(timestamp, username)
        executor.modify(args)
    elif action == "delete":
        executor = fileHandler.FileHandler(timestamp, username)
        executor.delete(args)
    elif action == "run":
        executor = processHandler.ProcessHandler(timestamp, username)
        executor.run(args)
    elif action == "help":
        printMenu()
    else:
        print("\n\'" + userInput + "\' is not a command.")
        print("Enter \'help\' to see available commands.\n")

    if executor:
        executor.log()

    return True


if __name__ == "__main__":
    main()
