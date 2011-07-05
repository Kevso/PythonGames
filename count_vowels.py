#!/usr/bin/env python
vowels = ['a','e','i','o','u', 'A', 'E', 'I', 'O', 'U']
candidate = str(raw_input('Gimme a string: '))
vowel_count = reduce(lambda accum, char: 
                     accum + (1 if char in vowels else 0), candidate, 0)

print 'There are ' + str(vowel_count) + ' in ' + candidate
