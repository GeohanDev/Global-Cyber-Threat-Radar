with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos_filter = text.find('class="filter-panel"')
end_filter = text.find('</section>', pos_filter)
print(text[pos_filter:end_filter])
