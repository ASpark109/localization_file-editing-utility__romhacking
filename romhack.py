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
    view = False
    q = input("View text block content? y/n: ")
    if q == 'y':
        view = True
    elif q == 'n':
        view = False
        
    file_view(file_name, addresses, view)

    #The user makes changes to the file
    os.system('cls')
    # hexgenerator()

    while input("Now you can put the generated" + Fore.GREEN + Style.BRIGHT + " hex " + Style.RESET_ALL + "values into the file. After that, click ok.\n") != 'ok': pass

    text_file_analyse("file_txt.txt", file_name, text_block_len_DEC)

    print("END")
    
    # return 0

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
    file = open(file_name, 'wb')

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

def hexgenerator():
    print(Fore.GREEN)
    art.aprint("seal")
    print(Style.RESET_ALL + "\nNow you can enter text and generate" + Fore.GREEN + Style.BRIGHT + " hex " + Style.RESET_ALL + "values. To exit, enter " + Fore.GREEN + Style.BRIGHT + "'uexit'" + Style.RESET_ALL)
    print("All generated values will be written to the" + Fore.GREEN + Style.BRIGHT + " newhex.txt " + Style.RESET_ALL + "file.\n")

    hex_file = open("newhex.txt", "w")

    while True:

        text = input("Your input:\n")

        if text == "uexit": 
            os.system('cls')
            break

        hex_file.write('\n\n' + text + '\n')

        print(Fore.GREEN + Style.BRIGHT)

        for item in text:
            if ord(item) < 256:
                item = '00' + hex(ord(item))[2:]
            elif ord(item) < 4096:
                item = '0' + hex(ord(item))[2:]
            else:
                item = hex(ord(item))[2:]

            item = item[2:] + item[:2]
            hex_file.write(item + " ")

            print(item, end=' ')
        print("\n" + Style.RESET_ALL)

#Displaying the contents of a text block in the console and writing to a file
def file_view(file_name, addresses, pr):

    # for item in addresses:
    #     print(item)
    # file = open(file_name, 'r', encoding='utf-16le')
    file = open(file_name, 'rb')
    text_file = open("file_txt.txt", 'w', encoding="utf-16")

    file.seek(34)
    prev = 0
    

    for i in range(len(addresses)):
        file.seek(prev + 34)
        a = file.read(addresses[i][0] - prev).decode('utf-16-le')
        prev = addresses[i][0]
        text_file.write('[{}]'.format(i) + a + '\n')

    file.close()
    text_file.close()

    input(Style.RESET_ALL + "\nA file" + Fore.GREEN + Style.BRIGHT + " (file_txt.txt) " + Style.RESET_ALL + "was created with the contents of the text block.\nTo continue, enter any character: ")

#Display information about the updated file
def view_updated_info(count, new_text_block_len_DEC, new_text_block_len_HEX, text_block_len_DEC):
    # os.system('cls')
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

def text_file_analyse(file, bnfile, length):
    text_file = open(file, 'r', encoding="utf-16")
    # text_file = open(file, 'br')
    
    str = ''

    new_add = []
    new_text_block = ''
    res = ''

    count = 0

    while True:
        a = text_file.read(1)
        
        if a == '':
            break

        if 0 == ord(a):
            pref = str.find("]", 0, 7)
            l = len(str) - pref
            str = str[pref+1:len(str)]
            # print("|" + str + "|", len(str))
            


            for s in str:
                u = hex(ord(s))[2:]

                if len(u) == 3:
                    u = u[1:] + "0" + u[:1]
                elif len(u) == 2:
                    u = u + "00"
                elif len(u) == 1:
                    u = u + "000"

                if count == 6:
                    print(s, " ", u)

                res += u

            res += "0000"
            new_text_block += res
                # print(res)
            # print(count, " >----------------------<")
            str = ''
            res = ''
            new_add.append(l*2)
            count += 1

        str += a
        
    print(count)

    text_file.close()
    # print(new_text_block)    
    # file1 = open("tes.b.write.bin", 'wb')

    # file1.write(bytearray.fromhex(new_text_block))

    bfile = open(bnfile, 'rb')


    data = list(bfile.read())

    footer = data[:]

    print(len(data))

    del data[34: 34 + length]

    header = data[:34]
    footer = data[34:]


    print(len(header),"<")
    print(len(footer),"<<")
    print(len(data))

    bfile.close()

    bfile = open(bnfile, 'wb')

    

    bfile.write(bytes(header))
    bfile.write(bytearray.fromhex(new_text_block))
    bfile.write(bytes(footer))

    bfile.close()

    return new_add


if __name__ == '__main__':
    main()
