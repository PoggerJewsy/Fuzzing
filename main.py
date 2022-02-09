import random
import os


# exec the binary and pipe the output in orig_output 


FILE_NAME = "./a.out" # change this

os.system(f"cp {FILE_NAME} {FILE_NAME}_fuzz")

def flip_byte(in_bytes):
	i = random.randint(0,len(in_bytes))
	c = chr(random.randint(0,0xFF))
	return in_bytes[:i]+c+in_bytes[i+1:]

def copy_binary():
	with open(FILE_NAME, "rb") as orig_f, open(f"{FILE_NAME}_fuzz", "wb") as new_f:
		new_f.write(flip_byte(orig_f.read()))

def compare(fn1, fn2):
	with open(fn1) as f1, open(fn2) as f2:
		return f1.read()==f2.read()

def check_output():
	os.system(f"(./{FILE_NAME}_fuzz > fuzz_output")
	return compare("orig_output", "fuzz_output")


def check_gdb():
	os.system(f"echo disassemble main | gdb {FILE_NAME}_fuzz > fuzz_gdb")
	return compare("orig_gdb", "fuzz_gdb")

def check_radare():
	os.system(f'echo -e "aaa\ns sym.main\npdf" | radare2 {FILE_NAME}_fuzz > fuzz_radare')
	return compare("orig_radare", "fuzz_radare")

while True:
	copy_binary()
	if check_output() and not check_gdb() and not check_radare():
		print ("FOUND POSSIBLE FAIL\n\n\n")
		os.system("tail fuzz_gdb")
		os.system("tail fuzz_radare")
		input()
