def wash_keywords():
    with open('seen_keywords.txt', 'r') as f:
        content = f.read()
    with open('wash_keywords.txt', 'w') as fp:
        for keywords in content.strip().split('\n'):
            if any(key in keywords.split() for key in
                   ['asphalt', 'crack', 'machine', 'equipment', 'cracks', 'driveway']):
                fp.write(keywords + '\n')


def hasnumbers(keywords):
    return any(char.isdigit() for char in keywords.split())


def wash_numbers():
    with open('wash_keywords.txt', 'r') as f:
        content = f.read()
    with open('result_keywords.txt', 'w') as fp:
        for keywords in content.strip().split('\n'):
            if not hasnumbers(keywords):
                fp.write(keywords + '\n')


wash_numbers()
