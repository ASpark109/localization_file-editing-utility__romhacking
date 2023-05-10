import art
import os
from colorama import init

from colorama import Fore, Back, Style
def main():
    init()

    print(Fore.GREEN + Style.BRIGHT)
    art.tprint("Welcome!")
    print(Style.RESET_ALL)

    file_name = file_select()
    #Таблиця для відступів від початку текстового блоку (адресів)
    addresses = []

    #Відкриваємо файл
    file = open(file_name, 'rb')

    # Читаємо довжину текстового блоку
    file.seek(22)
    u = file.read(2)
    text_block_len_HEX = hex(u[1])[2:] + hex(u[0])[2:]
    text_block_len_DEC = int(text_block_len_HEX, 16)

    #Стаємо на початок текстового блоку
    file.seek(34)

    #Починаємо шукати адреси (Відступ спочатку в десяткових числах)
    offset = 0
    for i in range(int(text_block_len_DEC/2)):
        step = file.read(2)
        offset += 2
        if hex(step[0])[2:] == '0':
            addresses.append([offset, None])

    #Конвертування десяткових чисел в шістнадцяткові
    for address in addresses:
        if address[0] < 256:
            address[1] = hex(address[0])[2:] + "00"
        elif address[0] < 4096:
            address[1] = hex(address[0])[3:] + "0" + hex(address[0])[2:3]
        elif address[0] < 65536:
            address[1] = hex(address[0])[4:] + hex(address[0])[2:4]

    #Кількість текстових блоків
    text_block_num = len(addresses)

    print(Fore.GREEN +"\n\nThe file is analysed:\n"+ Fore.RESET +
          "-----------------------\n"+
          "Number of addresses in a text block  " + Fore.CYAN + "{}\n".format(text_block_num) + Fore.RESET +
          "Length of the text block DEC         " + Fore.CYAN + "{}\n".format(text_block_len_DEC) + Fore.RESET +
          "Length of the text block HEX         " + Fore.CYAN + "{}\n".format(text_block_len_HEX))

    #Закриваєм проаналізований файл
    file.close()

    #Користувач вносить зміни в файл
        #TODO

    print(Fore.GREEN + "\nYou can now make changes to the file. After making changes, enter ok")
    while i != 'ok':
        i = input()

    #Відкриваємо файл для повторного аналізу
    file = open('strings_EN.dat.game.bin', 'rb')

    #Стаємо на початок текстового блоку
    file.seek(34)

    updated_addresses = []

    #Аналізуємо файл

    #Обнуляємо offset
    offset = 0
    count = 0

    while count < text_block_num:
        step = file.read(2)
        offset += 2
        if hex(step[0])[2:] == '0':
            count += 1
            updated_addresses.append([offset, None])
    # print("")
    # print("Кількість текстових блоків в оновленому файлі", count)

    #Конвертування десяткових чисел в шістнадцяткові для нових текстових блоків
    for address in updated_addresses:
        if address[0] < 256:
            address[1] = hex(address[0])[2:] + "00"
        elif address[0] < 4096:
            address[1] = hex(address[0])[3:] + "0" + hex(address[0])[2:3]
        elif address[0] < 65536:
            address[1] = hex(address[0])[4:] + hex(address[0])[2:4]

    #Нова довжина текстового блоку в десяткових числах
    new_text_block_len_DEC = offset
    # print("Довжина текстового блоку в оновленому файлі DEC", new_text_block_len_DEC)
    #Нова довжина текстового блоку в шістнадцяткових числах
    new_text_block_len_HEX = hex(offset)[2:4] + hex(offset)[4:]
    # print("Довжина текстового блоку в оновленому файлі HEX", new_text_block_len_HEX)

    print(Fore.GREEN + "\n\nThe changes in the file have been analyzed:\n" + Fore.RESET +
          "-----------------------\n"+
          "Number of addresses in a text block  " + Fore.CYAN + "{}\n".format(count) + Fore.RESET +
          "Length of the text block DEC         " + Fore.CYAN + "{}\n".format(new_text_block_len_DEC) + Fore.RESET +
          "Length of the text block HEX         " + Fore.CYAN + "{}\n".format(new_text_block_len_HEX) + Fore.RESET +
          "-----------------------\n" + Fore.GREEN +
          "In the text block of the updated file, " + Fore.CYAN + "{}".format(new_text_block_len_DEC-text_block_len_DEC) + Fore.GREEN + " characters were added" + Fore.RESET)

    #Читаєм файл повністю в пам'ять, для подальшої зміни
    file.seek(0)
    file_snapshot = list(file.read())

    #Записуємо нову довжину текстового блоку
    file_snapshot[22] = int(hex(offset)[4:],16)
    file_snapshot[23] = int(hex(offset)[2:4],16)


    #Стаємо на початок блоку кординат
    pointer = 33 + 12 + new_text_block_len_DEC

    #Починаємо записувати нові координати
    for i in range(text_block_num - 1):
        # print(file_snapshot[pointer+1], file_snapshot[pointer+2])
        file_snapshot[pointer + 1] = int(updated_addresses[i][1][:2], 16)
        file_snapshot[pointer + 2] = int(updated_addresses[i][1][2:], 16)
        # print(file_snapshot[pointer+1], file_snapshot[pointer+2])
        pointer += 8


    #Записуємо масив з оновленими данними в файл
    file = open('strings1_EN.dat.game.bin', 'wb')
    file1 = open('text.txt', 'w')

    for i in range(text_block_num):
        file1.write(str(addresses[i]) + '\t' +str(updated_addresses[i]) + '\t' + str(updated_addresses[i][0] - addresses[i][0]) + '\n')

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
    
    print("\nTo exit the application, press the q key")
    while i != 'q':
        i = input()


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
