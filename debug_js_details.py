with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- LINES 1660 TO 1705 ---")
for i in range(1660, 1705):
    print(f"{i+1}: {lines[i]}", end='')

print("\n--- LINES 1895 TO 1935 ---")
for i in range(1895, 1935):
    print(f"{i+1}: {lines[i]}", end='')
