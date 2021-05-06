# Telemetry Generator

This framework generates and records activity for the purpose of validating activity recorded by a Red Canary EDR agent. It 

## Installation
This program is written in Python3, so with Python installed, you can clone and install necessary dependencies using the following command.

```
git clone https://github.com/mabthew/telemetry_generator && 
    cd telemetry_generator &&
    pip install -r requirements.txta
```

## Usage
The framework exposes 5 functionalities.

`create <path> "[contents]"`: creates  a file given an absolute or relative path and optional contents.

`modify <path> "[contents]"`: appends to the end of an existing file or creates a new file with the provided text.

`delete <path>`: deletes a file given an absolute or relative path.

`run <command> [args...]`: executes the provided command and takes in optional arguments.

`send <address> <port> "[data]"`: establishes a tcp connection with the provided address and port and sends over data (optional).




## Implementation Details

### Handler Classes

I used python for this project because I wanted to use an object-oriented language. This allowed me to create a generic abstract superclass that all my other classes inherit from. With this constructor of this class, I initialize any variables shared across all of its subclasses. I also utilized an abstract method for logging so that all subclasses were forced to implement the method to fulfill their individual requirements. The superclass also has a method `getProcessInfo()` that is utilized the same by all subclasses.

This class structure allows for the code to easily be extended in the future to handle other types of activity generation and logging. One could simply create a new class that inherits the class I mentioned above, implement the `log()` function, and add whatever other type of activity they please.


### Logger

I implemented the logger as a singleton because I wanted only one instance of it to be in charge of manipulating the log file. I realize the singleton is a controversial pattern to many, but in the case of a logger, it seemed like a suitable implementation.


### Testing

I used python's unittest package to test my program's functionality. I structured my code to only execute logs when the handlers returned true. Because of this, I was able to test the log functionality separately from the handlers. 

## Notes

### Network calls

The instructions used the wording "establish a network connection and transmit data", so based on the word establish I implemented a TCP socket to transmit the data.

### Supported OS

I developed this on my a Mac and tested it on a Docker container running Linux to ensure that it worked on at least 2 platforms. I've included the Dockerfile I used for testing. It can be run using the following command.

```
docker build .  
docker run <image_id>
```
