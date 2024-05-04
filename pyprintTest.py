import os
import time


dlString = "https://firebasestorage.googleapis.com/v0/b/fileuploading-67153.appspot.com/o/files%2Fea7e9cb0-3747-4c8f-9a39-2b2bd09c2639?alt=media&token=39a9e8aa-6021-4c50-83dd-88f7de65e4f0"
fileName = "SFT-LETTER-TO-PARENTS.pdf"
printer = "shortBond_Gray"


# os.system("ls")
os.system(f"wget -O {fileName} {dlString}")

time.sleep(5)

os.system(f"lp -d {printer} {fileName}")

