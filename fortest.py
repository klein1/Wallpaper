import urllib.request

url = 'http://image.wufazhuce.com/FjBWkmVOMxbX9Vl5vdCKpm4udgKK'
web = urllib.request.urlopen(url)
data = web.read()
f = open('d:/a.png',"wb")
f.write(data)
f.close()
