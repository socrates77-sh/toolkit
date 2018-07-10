import re

ROM_SIZE = 0x2000
rom_file = '20171019chk-rcvref.rom'

rom = []


def init_rom_with_ff():
    for i in range(ROM_SIZE):
        rom.append(0xff)


def fill_one_line_data(line_txt):
    split_txt = line_txt.split()
    start_addr = split_txt[0][1:]
    line_data = split_txt[1:]
    for i in range(len(line_data)):
        rom[i + int(start_addr, 16)] = int(line_data[i], 16)


def fill_rom_from_file(romfile):
    init_rom_with_ff()
    lines = open(romfile).readlines()
    for l in lines:
        fill_one_line_data(l)


def main():
    fill_rom_from_file(rom_file)
    print(rom)

if __name__ == '__main__':
    main()
