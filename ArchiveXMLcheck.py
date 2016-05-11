import re
import binascii
import stat, os
import getopt, sys
import zlib, hashlib
import xml.etree.ElementTree as ET

def iterfile(f, bufSize):
	while True:
		data = f.read(bufSize)
		yield data
		if len(data) < bufSize:
			return

def crc32(f, bufSize):
	value = 0
	if not (bufSize):
		value = zlib.crc32(f.read()) & 0xffffffff
	else:
		for data in iterfile(f, bufSize):
			value = zlib.crc32(data, value) & 0xffffffff

	return int(value)

def hashloop(hashobj, f, bufSize):
	if not (bufSize):
		hashobj.update(f.read())
	else:
		for data in iterfile(f, bufSize):
			hashobj.update(data)

	return hashobj.digest()

def md5(f, bufSize):
	hashobj = hashlib.md5()
	return hashloop(hashobj, f, bufSize)

def sha1(f, bufSize):
	hashobj = hashlib.sha1()
	return hashloop(hashobj, f, bufSize)


def usage():
	print("./%s -i input-files.xml" % (sys.argv[0]))
	print("-b      => Sets buffer size to use on file (default is to load the whole file into memory)")
	print("-r      => Uses regex string to filter the files being hashed")
	print("--crc32 => Selects crc32 as the preferred hashing algorithm (Checksum, not a hash)")
	print("--sha1  => Selects sha1  as the preferred hashing algorithm (Secure, until proven otherwise!)")
	print("--md5   => Selects md5   as the preferred hashing algorithm (Proven otherwise ...)")

if (__name__ == "__main__"):
	try:
		longopts = ["crc32", "md5", "sha1"]
		opts, args = getopt.getopt(sys.argv[1:], "i:b:r:h", longopts)
	except getopt.GetoptError as error:
		print(error)
		usage()
		sys.exit(1)

	bufSize = 0
	infile = None
	pattern = None
	hashFunc = sha1
	hashName = "sha1"
	for (opt, arg) in opts:
		if (opt == "--crc32"):
			hashName = "crc32"
			hashFunc = crc32
		elif (opt == "--md5"):
			hashName = "md5"
			hashFunc = md5
		elif (opt == "--sha1"):
			hashName = "sha1"
			hashFunc = sha1
		elif (opt == "-r"):
			pattern = arg
		elif (opt == "-h"):
			usage()
			sys.exit(1)
		elif (opt == "-i"):
			infile = arg
		elif (opt == "-b"):
			bufSize = int(arg)
			if (bufSize < 0):
				print("-b must be zero or greater.")
				sys.exit(1)
		else:
			print("Unknown argument: %s" % opt)
			sys.exit(1)

	if (infile == None):
		print("Input file must be specified")
		print("")
		usage()
		sys.exit(1)
	else:
		archiveXMLtree = ET.parse(infile)
		root = archiveXMLtree.getroot()

	for elem in root.findall('file'):
		if (elem == None):
			print(elem)
			break
		name = elem.get('name')
		if (pattern != None):
			if not (re.match(pattern, name)):
				continue

		try:
			ret = elem.find('size')
			size = int(ret.text)
			try:
				fsize = os.stat(name).st_size
			except FileNotFoundError:
				print("DOES NOT EXIST: %s" % name)
				continue
		except AttributeError:
			continue

		textbin = elem.find(hashName).text
		hashbin = binascii.unhexlify(textbin)

		if (fsize != size):
			print("Mismatched file size on: %s" % name)
			continue

		with open(name, "rb") as f:
			fhash = hashFunc(f, bufSize)
			if (hashName == "crc32"):
				if (fhash != int(textbin, 16)):
					print("BAD HASH: %s" % name)
				else:
					print("VERFIED: %s" % name)
			elif (fhash != hashbin):
				print("BAD HASH: %s" % name)
			else:
				print("VERFIED: %s" % name)





