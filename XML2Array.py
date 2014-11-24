import xml.etree.ElementTree as ET

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
  return a