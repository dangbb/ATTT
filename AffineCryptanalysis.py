S = "adsfgds"

count_vector = {}
prob_ref = {
    'e': 0.127,
    't': 0.091,
    'a': 0.082,
    'o': 0.075,
    'i': 0.070,
    'n': 0.057,
    's': 0.063,
    'h': 0.061,
    'r': 0.060
}

for c in S:
    if ord(c) - 97 not in count_vector.keys():
        count_vector[ord(c) - 97] = 1
    else:
        count_vector[ord(c) - 97] += 1

for i in range(26):
    if i not in count_vector.keys():
        count_vector[i] = 0
    count_vector[i] = count_vector[i] / len(S)

sorted(count_vector, key=count_vector.get)

print(count_vector)




