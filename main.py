import fileHandler
import processHandler


def main():
    running = True

    printOptions()
    while running:
        userInput = input("command: ")
        action, args = parseInput(userInput)

        if action == "quit":
            running = False
        elif action == "create":
            fileHandler.FileHandler().create(args)
        elif action == "modify":
            fileHandler.FileHandler().modify(args)
        elif action == "delete":
            fileHandler.FileHandler().delete(args)
        elif action == "run":
            processHandler.ProcessHandler().run(args)
        elif action == "help":
            printOptions()
        else:
            print("\n\'" + userInput + "\' is not a command.")
            print("Enter \'help\' to see available commands.\n")


def printOptions():
    print("\nTelemetry generator: framework that generates and logs endpoint activity.")

    print("\nOptions:")
    print("\t\'create [filename]\' \t\t Create a new file.")
    print("\t\'modify [filename] [content]\' \t Modify a file.")
    print("\t\'delete [filename]\' \t\t Delete a file.")
    print("\t\'help\' \t\t\t Show this message.")
    print("\t\'quit\' \t\t\t Exit program.\n")


def parseInput(input):
    parsedInput = input.split(' ')

    return parsedInput[0], ' '.join(parsedInput[1:])


if __name__ == "__main__":
    main()
