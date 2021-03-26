from PIL import Image
import io
import re


file=open(r"C:\Users\ftom7\OneDrive\Pictures\3.jpg","rb")
content=file.read()
file.close()
content="image: "+content.decode('latin-1')
content=content.encode("utf-8")
content=content.decode("utf-8")
message=re.search("([\s\S]*?): ([\s\S]*)",content)
Image.open(io.BytesIO(bytes(message.group(2),'latin-1'))).show()
