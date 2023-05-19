import art
import os
from colorama import init

from colorama import Fore, Back, Style
def main():
    init()
    os.system('cls')
    titel("Welcome!")

    file_name = file_select()
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

    view_info(text_block_num, text_block_len_DEC, text_block_len_HEX)

    #Close the analysed file
    file.close()

    #If the user wants, we display the contents of the text block and write it to the file
    if input("View text block content? y/n: ") == 'y':
        file_view(file_name, addresses)

    #The user makes changes to the file
    os.system('cls')
    art.aprint("seal")
    print(Fore.GREEN + "\nYou can now make changes to the file. After making changes, enter ok")
    while i != 'ok':
        i = input()

    #Open the modified file for re-analysis
    file = open('strings_EN.dat.game.bin', 'rb')

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
    view_updated_info(count, new_text_block_len_DEC, new_text_block_len_HEX, text_block_len_DEC)

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


    #Write an array with updated data to the file
    file = open('strings1_EN.dat.game.bin', 'wb')

    u = None
    for i in range(504, 509):
        f =  hex(file_snapshot[i])[2:]
        if(file_snapshot[i] < 16):
            f  = '0' + f

    q = 0
    for point in range(len(file_snapshot)):
        q+=1
        u = hex(file_snapshot[point])[2:]

        if(file_snapshot[point] < 16):
            u  = '0' + u
        
        test = u
        if(q == 16):
            q = 0
            test += '\n'
        else:
            test += ' '

        file.write(bytearray.fromhex(u))
        
    file.close()
    os.system('cls')
    print("\nTo exit the application, press the q key")
    while i != 'q':
        i = input()

#Displaying the contents of a text block in the console and writing to a file
def file_view(file_name, addresses):
    file = open(file_name, 'r', encoding='ISO-8859-1')
    text_file = open("file_txt.txt", 'w', encoding="ISO-8859-1")

    file.seek(34)

    previous = 0
    
    for i in range(len(addresses)):
        str = file.read(addresses[i][0] - previous)
        previous = addresses[i][0]
        text_file.write('[{}][{}]   '.format(addresses[i][0], i) + str[::2] + '\n')
        print(Fore.GREEN + Style.BRIGHT + "[{}] ".format(i) + Style.RESET_ALL,str + '\n')

    file.close()
    text_file.close()

    input("\nA file" + Fore.GREEN + Style.BRIGHT + " (file_txt.txt) " + Style.RESET_ALL + "was created with the contents of the text block.\nTo continue, enter any character: ")

#Display information about the updated file
def view_updated_info(count, new_text_block_len_DEC, new_text_block_len_HEX, text_block_len_DEC):
    os.system('cls')
    titel("Great!")
    print(Fore.GREEN + "The changes in the file have been analyzed:\n" + Fore.RESET +
          "-----------------------\n"+
          "Number of addresses in a text block  " + Fore.CYAN + "{}\n".format(count) + Fore.RESET +
          "Length of the text block DEC         " + Fore.CYAN + "{}\n".format(new_text_block_len_DEC) + Fore.RESET +
          "Length of the text block HEX         " + Fore.CYAN + "{}\n".format(new_text_block_len_HEX) + Fore.RESET +
          "-----------------------\n" + Fore.GREEN +
          "In the text block of the updated file, " + Fore.CYAN + "{}".format(new_text_block_len_DEC-text_block_len_DEC) + Fore.GREEN + " characters were added" + Fore.RESET)
    input("\nTo continue, enter any character: ")

#Displaying information about the analysed file
def view_info(text_block_num, text_block_len_DEC, text_block_len_HEX):
    os.system('cls')
    titel("Done!")
    print(Fore.GREEN +"The file is analysed:\n"+ Fore.RESET +
          "-----------------------\n"+
          "Number of addresses in a text block  " + Fore.CYAN + "{}\n".format(text_block_num) + Fore.RESET +
          "Length of the text block DEC         " + Fore.CYAN + "{}\n".format(text_block_len_DEC) + Fore.RESET +
          "Length of the text block HEX         " + Fore.CYAN + "{}\n".format(text_block_len_HEX))

#Function for displaying large text (art)
def titel(str):
    print(Fore.GREEN + Style.BRIGHT)
    print(art.text2art(str))
    print(Style.RESET_ALL)


def file_select():
    # folder path
    dir_path = r'.\\'

    # list to store files
    menu = []

    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            menu.append(path)

    for i in range(len(menu)):
        print(Fore.YELLOW + "[{}] {}".format(i, menu[i]) + Fore.RESET)
    
    file_name = input("\nPlease select a file ")
    
    return menu[int(file_name)]

if __name__ == '__main__':
    main()
