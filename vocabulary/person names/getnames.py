with open('census-derived-all-first.txt', 'r') as myfile:
    data=myfile.read()
data = data.split()
with open("names.txt", "w") as text_file:
  for i in range(len(data)//4):
    print('-',data[i*4])
    text_file.write(data[i*4]+'\n')
print(range(len(data)//4))
