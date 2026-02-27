with open('bu_org_emails.txt', 'r') as f:
    orgs = f.read().strip().split('\n')

def random_sample_org():
    import random
    x = []
    for i in range(20):
        x.append(orgs.pop(random.randint(0, len(orgs) - 1)))
    return x

print(random_sample_org())
with open('random_sample_orgs.txt', 'w') as f:
    for org in random_sample_org():
        f.write(org + '\n')