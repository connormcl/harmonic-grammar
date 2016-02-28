# Connor McLaughlin
#
# Implementation of the Gradual Learning Algorithm for Harmonic Grammar

import sys
import re
import random

grammar_file = open(sys.argv[1])
data_file = open(sys.argv[2])
uni = int(sys.argv[3])
iterations = int(sys.argv[4])
rate = float(sys.argv[5])
grammar = {}
constraints = []
data = []
weights = []
sum_of_relative_frequencies = 0

curr_input = ''
for line in grammar_file.readlines():
    m = re.match('constraint\t\[\d*\]:\t(.*)\r?', line)
    if m:
        constraints.append(str(m.group(1)))
    m = re.match('input\t\[\d*\]:\t([CV]*)', line)
    if m:
        curr_input = m.group(1)
        grammar[curr_input] = {}
    m = re.match('\s*candidate\t\[\d*\]:\t([CV]*)\s*([\t\d]*)', line)
    if m:
        grammar[curr_input][m.group(1)] = map(int, m.group(2).split('\t'))

for line in data_file.readlines():
    m = re.match('([CV]+)\s*([CV]+)\s*(\d*)', line)
    if m:
        data.append((m.group(1), m.group(2), m.group(3)))

if uni == 0:
    for c in constraints:
        markedness = int(c.split('\t')[1])
        if markedness == 1:
            weights.append(10.0)
        else:
            weights.append(1.0)
elif uni == 1:
    for c in constraints:
        weights.append(1.0)
else:
    print 'UNI must be either 0 or 1'
    exit()

for datum in data:
    sum_of_relative_frequencies += int(datum[2])


def harmony(violations, weights):
    harmony = 0.0
    for i in range(0, len(weights)):
        harmony -= weights[i] * float(violations[i])
    return harmony


def optimize(weights, grammar, pInput):
    optimal_output = pInput
    optimal_harmony = harmony(grammar[pInput][optimal_output], weights)
    outputs = grammar[pInput].keys()
    h = optimal_harmony
    for o in outputs:
        h = harmony(grammar[pInput][o], weights)
        if h > optimal_harmony:
            optimal_harmony = h
            optimal_output = o
    return optimal_output


def next_datum(data):
    r = random.randint(1, sum_of_relative_frequencies)
    datum = (data[0][0], data[0][1])
    if r > int(data[0][2]):
        frequency_sum = int(data[0][2])
        for i in range(1, len(data)):
            if r <= int(data[i][2]) + frequency_sum:
                datum = (data[i][0], data[i][1])
                break
            else:
                frequency_sum += int(data[i][2])
    return datum


def compute_change_vector(error, target):
    v = []
    for i in range(0, len(error)):
        v.append(round((float(error[i]) * rate) - (float(target[i]) * rate), 1))
    return v


def add_vectors(source, change):
    v = []
    for i in range(0, len(source)):
        v.append(source[i] + float(change[i]))
    return v


def update(datum, grammar, weights, rate):
    pInput = datum[0]
    target = datum[1]
    output = optimize(weights, grammar, pInput)
    if output != target:
        print 'ERROR: Datum is\t' + datum[0], datum[1] + '\tOUTPUT is\t' + output
        change_vector = compute_change_vector(grammar[pInput][output], grammar[pInput][target])
        weights = add_vectors(weights, change_vector)
    return weights


def evaluate(weights, grammar, data):
    correct_count = 0
    for datum in data:
        output = optimize(weights, grammar, datum[0])
        print 'data:\t' + datum[0], datum[1] + '\tOUTPUT', output
        if datum[1] == output:
            correct_count += 1
    print 'ACCURACY is\t' + str(float(correct_count)/len(data))


print 'CURRENT GRAMMAR:\t', weights
evaluate(weights, grammar, data)
print 'ITERATION\t', 0

for i in range(1, iterations+1):
    w = update(next_datum(data), grammar, weights, rate)
    if w != weights:
        weights = w
        sys.stdout.write('CURRENT GRAMMAR:\t[')
        sys.stdout.write("%.1f" % weights[0])
        for j in range(1, len(weights)):
            sys.stdout.write(", %.1f" % weights[j])
        print ']'
        evaluate(weights, grammar, data)
    print 'ITERATION\t', i

grammar_file.close()
data_file.close()
