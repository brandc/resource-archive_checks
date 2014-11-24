def confirmFiles(files):
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