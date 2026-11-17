"""
file=open("example_L.W.Yu.txt","r")
content=file.readlines()
length=len(content)
print(content[length-1])
file.close()
"""

file=open("example_L.W.Yu.txt","a")
#file.write("byebye L.W.Yu!")
#file.write("byebye L.W.Yu!\n")
file.write("123456\n")

file.close()
