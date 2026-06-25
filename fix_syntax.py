import glob

files = glob.glob('**/*.py', recursive=True)
fixed = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    # Replace escaped triple quotes \" \" \" with real triple quotes
    new_content = content.replace('\\"\\"\\"', '"""')
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        fixed.append(f)

print('Fixed files:')
for f in fixed:
    print(' -', f)
print(f'Total: {len(fixed)} files fixed')
