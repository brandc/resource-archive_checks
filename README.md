![Programming Language](https://img.shields.io/badge/Python-Programming%20Language-brightgreen)
![Zero Clause BSD License](https://img.shields.io/badge/License-BSD%20Zero%20Clause-green)

# Resource Archive Checks
Verifies the manifests against the files from archive.org given their respective XML file.

# Usage
To run all checks for a given manifest file
```
python3 ArchiveXMLcheck.py --sha1 --crc32 --md5 -i input.xml
```

You can also use --sha1, --crc32, and/or --md5 in any combination if you want to ensure file integrity with multiple checksums/hashes

# Requirements:
- Python

# License
All code and files in this repository are licensed under the 0-BSD License
