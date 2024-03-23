from wcwidth import wcswidth

# Function to pad a string to a specified width
def pad_string(s, width):
    needed_padding = width - wcswidth(s)
    # Adding space padding to the right of the string
    return s + ' ' * needed_padding

# Read the file and split into lines and columns
with open('./res/p1.txt', 'r', encoding='utf-8') as f:
    lines = [line.strip().split(' ') for line in f]

# Since the number of columns can vary, find the maximum number of columns in any row
max_columns = max(len(line) for line in lines)

# Initialize a list to hold the maximum width for each column, filled with zeroes
max_widths = [0] * max_columns

# Calculate the maximum display width for each column
for line in lines:
    for i, item in enumerate(line):
        item_width = wcswidth(item)
        if item_width > max_widths[i]:
            max_widths[i] = item_width

# Create the aligned output
aligned_lines = []
for line in lines:
    aligned_line = [pad_string(item, max_widths[i]) for i, item in enumerate(line)]
    # For rows with fewer columns, append additional spaces as needed
    for i in range(len(line), max_columns):
        aligned_line.append(' ' * max_widths[i])
    aligned_lines.append(' '.join(aligned_line))

# Optionally, write the aligned lines back to a file
with open('aligned_file.txt', 'w', encoding='utf-8') as f:
    for line in aligned_lines:
        f.write(line + '\n')
