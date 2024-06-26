import art
import os
from colorama import init
from datetime import datetime

from colorama import Fore, Back, Style

def main():
    init()
    os.system('cls')
    author()
    titel(" Welcome!")

    file_name = file_select()
    content_file_name = "file_txt.txt"
    #Table for indentation from the beginning of a text block (address table)
    addresses = []

    #Open a file for reading in binary format
    file = open(file_name, 'rb')

    #Read the length of the text block (2 bytes)
    file.seek(22)
    u = file.read(2)
    text_block_len_HEX = hex(u[1])[2:] + hex(u[0])[2:]
    text_block_len_DEC = int(text_block_len_HEX, 16)

    #Go to the beginning of the text block
    file.seek(34)

    #Start looking for addresses (length in bytes of each text block)
    offset = 0
    for i in range(int(text_block_len_DEC/2)):
        step = file.read(2)
        offset += 2
        if hex(step[0])[2:] == '0':
            addresses.append([offset, None])

    #Convert decimal numbers to hexadecimal, also write to addresses
    for address in addresses:
        if address[0] < 256:
            address[1] = hex(address[0])[2:] + "00"
        elif address[0] < 4096:
            address[1] = hex(address[0])[3:] + "0" + hex(address[0])[2:3]
        elif address[0] < 65536:
            address[1] = hex(address[0])[4:] + hex(address[0])[2:4]

    #Number of text blocks
    text_block_num = len(addresses)

    file_info(text_block_num, text_block_len_DEC, text_block_len_HEX)

    #Close the analysed file
    file.close()
  
    content_file_create(file_name, addresses, content_file_name)

    #The user makes changes to the file
    os.system('cls')

    text_block_replace(content_file_name, file_name, text_block_len_DEC)
    
    file_analysing_and_adresses_overwriting(file_name, text_block_num, text_block_len_DEC)

def file_analysing_and_adresses_overwriting(file_name, text_block_num, text_block_len_DEC):
    #Open the modified file for re-analysis
    file = open(file_name, 'rb')

    #Go to the beginning of the text block
    file.seek(34)

    updated_addresses = []

    #Reset offset
    offset = 0
    count = 0

    while count < text_block_num:
        step = file.read(2)
        offset += 2
        if hex(step[0])[2:] == '0':
            count += 1
            updated_addresses.append([offset, None])

    #Convert decimal numbers to hexadecimal for new text blocks
    for address in updated_addresses:
        if address[0] < 256:
            address[1] = hex(address[0])[2:] + "00"
        elif address[0] < 4096:
            address[1] = hex(address[0])[3:] + "0" + hex(address[0])[2:3]
        elif address[0] < 65536:
            address[1] = hex(address[0])[4:] + hex(address[0])[2:4]

    new_text_block_len_DEC = offset
    new_text_block_len_HEX = hex(offset)[2:4] + hex(offset)[4:]

    #View updated information
    updated_file_info(count, new_text_block_len_DEC, new_text_block_len_HEX, text_block_len_DEC)

    #Read the entire file into memory for further modification
    file.seek(0)
    file_snapshot = list(file.read())

    #Write down the new length of the text block
    file_snapshot[22] = int(hex(offset)[4:],16)
    file_snapshot[23] = int(hex(offset)[2:4],16)


    #Stand at the beginning of the cordinate block
    pointer = 33 + 12 + new_text_block_len_DEC

    #Start recording new coordinates
    for i in range(text_block_num - 1):
        file_snapshot[pointer + 1] = int(updated_addresses[i][1][:2], 16)
        file_snapshot[pointer + 2] = int(updated_addresses[i][1][2:], 16)
        pointer += 8

    file.close()

    #Write an array with updated data to the file
    file = open(file_name, 'wb')

    file.write(bytes(file_snapshot))
        
    file.close()

    input(" To exit, enter any character: ")

#Displaying the contents of a text block in the console and writing to a file
def content_file_create(file_name, addresses, content_file_name):
    file = open(file_name, 'rb')
    text_file = open(content_file_name, 'w', encoding="utf-16")

    file.seek(34)
    prev = 0
    

    for i in range(len(addresses)):
        file.seek(prev + 34)
        a = file.read(addresses[i][0] - prev).decode('utf-16-le')
        prev = addresses[i][0]
        text_file.write('[{}]'.format(i) + a + '\n')

    text_file.close()
    file.close()
    
    print(Style.RESET_ALL + "\n A file" + Fore.GREEN + Style.BRIGHT + " (" + content_file_name + ") " + Style.RESET_ALL + 
        "was created with the contents of the text block.\n Now you can make changes to this text file. Please use a " + Fore.GREEN + Style.BRIGHT + "Notepad++" + Style.RESET_ALL + " to make changes.\n\n Type" + Fore.GREEN + Style.BRIGHT + " ok "  + Style.RESET_ALL + "at the end:", end="")

    while input(" ") != "ok": pass

#Display information about the updated file
def updated_file_info(count, new_text_block_len_DEC, new_text_block_len_HEX, text_block_len_DEC):
    titel(" Great!")
    print(Fore.GREEN + " The changes in the file have been analyzed:\n" + Fore.RESET +
          " -----------------------\n"+
          " Number of addresses in a text block  " + Fore.CYAN + "{}\n".format(count) + Fore.RESET +
          " Length of the text block DEC         " + Fore.CYAN + "{}\n".format(new_text_block_len_DEC) + Fore.RESET +
          " Length of the text block HEX         " + Fore.CYAN + "{}\n".format(new_text_block_len_HEX) + Fore.RESET +
          " -----------------------\n" + Fore.GREEN +
          " In the text block of the updated file, " + Fore.CYAN + "{}".format(round((new_text_block_len_DEC-text_block_len_DEC)/2)) + Fore.GREEN + " characters were added\n\n\n" + Fore.RESET)

#Displaying information about the analysed file
def file_info(text_block_num, text_block_len_DEC, text_block_len_HEX):
    titel(" Done!")
    print(Fore.GREEN +" The file is analysed:\n"+ Fore.RESET +
          " -----------------------\n"+
          " Number of addresses in a text block  " + Fore.CYAN + "{}\n".format(text_block_num) + Fore.RESET +
          " Length of the text block DEC         " + Fore.CYAN + "{}\n".format(text_block_len_DEC) + Fore.RESET +
          " Length of the text block HEX         " + Fore.CYAN + "{}\n".format(text_block_len_HEX) + Fore.RESET +
          " -----------------------\n")

#Function for displaying large text (art)
def titel(str):
    print(Fore.GREEN + Style.BRIGHT)
    print(art.text2art(str))
    print(Style.RESET_ALL)

def file_select():
    while True:
        # folder path
        dir_path = r'.\\'

        # list to store files
        menu = []
        file_name = ""

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                menu.append(path)

        for i in range(len(menu)):
            print(Fore.YELLOW + " [{}] {}".format(i, menu[i]) + Fore.RESET)
        
        file_name = input("\n Please select a file ")
        
        file = open(menu[int(file_name)], "rb")
        c = file.read(14).hex()
        file.close()

        if c == "07000000090000004c4353540200":
            os.system('cls')
            return menu[int(file_name)]
        else:
            os.system('cls')
            print(Fore.GREEN + " We're sorry, an error has occurred. The file you selected cannot be processed. You may have made a mistake, please try again\n" + Fore.RESET)

def text_block_replace(file, bnfile, length):

    #Open a text file
    text_file = open(file, 'br')
    str = ''
    res = ''

    count = 0

    #Skip the text file header
    text_file.read(2)

    #Reading text
    while True:
        while text_file.read(2).hex() != "5d00":
            pass
        while True:
            str = text_file.read(2).hex()
            
            if str != "0d00":
                res += str
            if str == "0000":
                count += 1
                break
        if count == 410:
            break

    text_file.close()

    #Open the main (you can create a copy) binary file in bitwise mode
    bfile = open(bnfile, 'rb')

    #Reading the data
    data = list(bfile.read())

    #Delete the text block
    del data[34: 34 + length]

    #Divide the content into header and footer (parts that come before and after the text block)
    header = data[:34]
    footer = data[34:]

    bfile.close()

    #Open a file in bitwise writing mode
    bfile = open(bnfile, 'wb')

    #Create a file from a header, an updated text block, and a footer
    bfile.write(bytes(header))
    bfile.write(bytearray.fromhex(res))
    bfile.write(bytes(footer))

    bfile.close()

def author():

    main_file_name = "romhack"
    date = ""

    for item in os.listdir(r'.\\'):
        if item == main_file_name + ".py":
            date = str(datetime.fromtimestamp(os.path.getmtime("romhack.py"))) + "   (version in development)"
            break
        if item == main_file_name + ".exe":
            date = str(datetime.fromtimestamp(os.path.getctime("romhack.exe"))) + "   (release version)"
            break

    print(Fore.GREEN + 
          " --------------------------------------\n" +
          " Authors: Liubomyr Kulka, Yurii Oliinyk\n" +
          " Source: https://github.com/ASpark109/localization_file-editing-utility__romhacking.git\n" +
          " Last update: ", date,"\n\n" +
          " This utility was created for the Soul Bubble game,\n and the software is completely open source and available for use by anyone.\n If you have any suggestions for the software, you can contribute to the repository.\n\n" +
          " Thanks! ", end="")
    art.aprint("seal")

    print(" --------------------------------------\n" + Fore.RESET)
          

if __name__ == '__main__':
    main()