import sys, os
import xml.etree.ElementTree as ET
import zlib, hashlib


def XML2Array(filename):
  tree = ET.parse(filename)
  root = tree.getroot()
  a = []
  for f in root.findall('file'):
    d = {}
    try:
      d['name'] = f.get('name')
      d['size'] = int(f.find('size').text)
      d['md5']  = f.find('md5').text
      d['crc32'] = f.find('crc32').text
      d['sha1'] = f.find('sha1').text
      a.append(d)
    except:
      continue
  return adef confirmFiles(files):
  absent = []
  broken = []
  confirmed = []
  for f in files:
    try:
      if f['size'] == os.stat(f['name']).st_size:
        confirmed.append(f)
      else:
        broken.append(f)
    except:
      absent.append(f)
  return (absent, broken, confirmed)

# If you put false for any of the hashes, the default value will be returned.
def checksumFile(f, bufsize, CRC32, MD5, SHA1):
  if bufsize < 1:
    bufsize = -1
  try:
    fi = open(f['name'], 'rb')
  except:
    print("Failed to open %s" % f['name'])

  c = 0
  m = hashlib.md5()
  s = hashlib.sha1()

  while (True):
    buf = fi.read(bufsize)
    if len(buf) == 0:
      break
    else:
      if CRC32 == True:
        c = zlib.crc32(buf, c)
      if MD5 == True:
        m.update(buf)
      if SHA1 == True:
        s.update(buf)

  fi.close()
  c = hex(c)
  c = c[2:]
  return (c, m.hexdigest(), s.hexdigest())

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
    (CRC32, MD5, SHA1) = checksumFile(f, -1, True, True, True)

    if (CRC32 == f['crc32']) and (MD5 == f['md5']) and (SHA1 == f['sha1']):
      print("PASSED: %s" % f['name'])
      passed.append(f)
    else:
      print("FAILED: %s" % f['name'])
      failed.append(f)

















