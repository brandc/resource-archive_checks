import zlib, hashlib

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