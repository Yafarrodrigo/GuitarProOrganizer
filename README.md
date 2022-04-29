# Guitar Pro Organizer

This tool attempts to organize guitar pro files by tuning
It only works with `.gp3` `.gp4` `.gp5` files at the moment.

---
## How to use

To use it move `gpo.py` to the folder with all the guitar pro files and run it.

**Usage**: ` python gpo.py [action] [outputFile] `

**action must be:**
    -C to copy the files
    -M to move the files
    -A to do nothing but Analyze the files

**outputFile** (*optional*): add the flag -F if you want the results in a text file

Also you can run it with t he flag -H to see how should be used.

---
## Supported Tunings
- Standard E
- Standard Eb
- Standard D
- Standard C
- Standard B
- Drop D
- Drop Db
- Drop C
- Drop B


---
## Dependencies

- [PyGuitarPro](https://github.com/Perlence/PyGuitarPro)