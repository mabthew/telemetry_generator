from handlers import fileHandler
from handlers import processHandler
import datetime
import os
import pwd
import subprocess


def main():
    running = True

    printMenu()
    while running:
        try:
            userInput = input("command: ")
            running = executeCommand(userInput)
        except KeyboardInterrupt:
            return


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
    print(
        "\t\'create <filename> \"[content]\"\'  Create a new file.")
    print("\t\'modify <filename> \"[content]\"\'  Create or append to a file.")
    print("\t\'delete <filename>\' \t\t Delete a file.")
    print("\t\'run <command> [args...]\' \t Execute a command.")
    print("\t\'help\' \t\t\t\t Show this message.")
    print("\t\'exit\' \t\t\t\t Exit program.\n")


def parseInput(input):
    parsedInput = input.split(' ')

    return parsedInput[0], ' '.join(parsedInput[1:])


def executeCommand(userInput):
    action, args = parseInput(userInput)

    # get call info
    timestamp = datetime.datetime.now()
    username = pwd.getpwuid(os.getuid())[0]

    executor = None
    success = False
    if action == "exit":
        return False
    elif action == "create" or action == "modify" or action == "delete":
        executor = fileHandler.FileHandler(timestamp, username)
        success = executor.call(action, args)
    elif action == "run":
        executor = processHandler.ProcessHandler(timestamp, username)
        success = executor.run(args)
    elif action == "help":
        printMenu()
    else:
        print("\n\'" + userInput + "\' is not a command.")
        print("Enter \'help\' to see available commands.\n")

    if executor and success:
        executor.log()

    return True


if __name__ == "__main__":
    main()
