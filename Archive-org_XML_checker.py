import sys, os
from ChecksumFile import *
from ConfirmFile import *
from XML2Array import *

# essentially the main() function
if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Requires XML input file.")

  files = XML2Array(sys.argv[1])
  (absent, broken, confirmed) = confirmFiles(files)
  print("Size matched files:")
  print(" Confirmed: %4d" % len(confirmed))
  print(" Absent:    %4d" % len(absent))
  print(" Broken:    %4d" % len(broken))
  passed = []
  failed = []
  for f in confirmed:
    c = False
    m = False
    s = False
    (CRC32, MD5, SHA1) = checksumFile(f, -1, True, True, True)
    if CRC32 == f['crc32']:
      c = True
    if MD5 == f['md5']:
      m = True
    if SHA1 == f['sha1']:
      s = True

    if (c == True) and (m == True) and (s == True):
      print("PASSED: %s" % f['name'])
      passed.append(f)
    else:
      print("FAILED: %s" % f['name'])
      failed.append(f)

















