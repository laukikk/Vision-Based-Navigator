import os
from gtts import gTTS
  
fh = open("test.txt", "r")
myText = fh.read().replace("\n", " ")
print(myText)
  
# Language we want to use 
language = 'en'
  

output = gTTS(text=myText, lang=language)
  

output.save("output.mp3") 
fh.close()
  
# Play the converted file 
os.system("start output.mp3")