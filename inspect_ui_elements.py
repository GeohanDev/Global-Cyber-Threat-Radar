with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('5-YEAR & CONTINUOUS')
print("Position of '5-YEAR & CONTINUOUS':", pos)
if pos != -1:
    print(text[pos-200:pos+200])

pos_filter = text.find('class="filters-section"')
if pos_filter == -1:
    pos_filter = text.find('class="filter')
print("\nFilters area:", pos_filter)
if pos_filter != -1:
    print(text[pos_filter:pos_filter+800])
