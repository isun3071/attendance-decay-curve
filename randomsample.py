import random

def random_sample_org(file='remaining_orgs.txt'):
    with open(file, 'r') as f:
        orgs = f.read().strip().split('\n')
    print(len(orgs))
    x = []
    for i in range(10):
        x.append(orgs.pop(random.randint(0, len(orgs) - 1)))
    print(len(orgs))
    with open(file, 'w') as f:
        f.write('\n'.join(orgs))
    return x
    

y = random_sample_org()
print(y)
with open('random_sample_orgs.txt', 'w') as f:
    for org in y:
        f.write(org + '\n')


with open('sent_orgs.txt', 'a') as f:
    for org in y:
        f.write(org + '\n')