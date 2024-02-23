def wrap_text(line, max_length=75):
    if len(line) <= max_length:
        return line
    
    split_index = line.rfind(" ", 70, max_length)
    if split_index == -1:
        split_index = max_length
    
    return line[:split_index].strip() + '\n' + wrap_text(line[split_index:].strip(), max_length)

# Example usage:
line = "Dr. Gnanam, a pillar of our community, was recognized and honored with a memento."
wrapped_text = wrap_text(line)
print(wrapped_text)
