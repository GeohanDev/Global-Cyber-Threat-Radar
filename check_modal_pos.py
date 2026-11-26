with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="articleReaderModal"')
print('Position of id="articleReaderModal":', pos)
if pos != -1:
    print("SURROUNDING 500 CHARACTERS:")
    print(text[pos-100:pos+400])
else:
    print("NOT FOUND AT ALL!")
