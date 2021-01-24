#!/usr/bin/python
import getopt
import sys
import copy
from asm6502 import asm6502

def ReadTextFileToArray(filename):
  fp = open(filename, "r") #opens the file in read mode
  lines = fp.read().splitlines() #puts the file into an array
  fp.close()
  return lines
  
def Usage():
  print("as65.py Version 1.0.0")
  print("Usage:   python3 as65.py -i [source_file] -o [bin_file] --base [rom_start] --size [rom_size]")
  print("Example: python3 as65.py -i as65_test.asm -o as65_test.bin --base 0xE000 --size 0x2000")
  
def Main():
  global VerboseFlag
  
  InputFile = False
  OutputFile = False
  OutputBase = 0
  OutputSize = 0x10000
  
  try:
    opts, args = getopt.getopt(sys.argv[1:], "i:o:b:s:thvl:", ["help", "input=", "output=", "base=", "size="])
  except getopt.GetoptError as err:
    print(str(err)) # will print something like "option -a not recognized"
    Usage()
    sys.exit(2)
  for command, arg in opts:
    if command == "-v":
      VerboseFlag = True
    elif command in ("-i", "--input"):
      SourceFile = arg
    elif command in ("-o", "--output"):
      OutputFile = arg
    elif command in ("--base"):
      OutputBase = int(arg, 16)
    elif command in ("--size"):
      OutputSize = int(arg, 16)
    elif command in ("-t", "--test"):
      TestFlag = True;
    elif command in ("-h", "--help"):
      Usage()
      sys.exit()
    else:
      assert False, "unhandled option"
  
  if SourceFile == False:
    print("Error: -i is required");
    Usage()
    sys.exit(2)
  
  if OutputFile == False:
    print("Error: -o is required");
    Usage()
    sys.exit(2)
    
  lines = ReadTextFileToArray(SourceFile)
  aobj = asm6502(debug=0)
  aobj.assemble(lines)
  #
  # Byte normalize
  #
  output_buffer = list()  # 64 K entries to cover whole memory map
  for i in range(0, OutputSize):
    c = aobj.object_code[OutputBase+i]
    if c == -1:
      c = 255
    output_buffer.append(c)
  #
  # Write binary buffer to file
  #
  fp = open(OutputFile, "wb")
  binary_array = bytearray(output_buffer)
  fp.write(binary_array)

if __name__ == "__main__":
  Main()