s = 'Evelop'.lower()
glas = set('aeiyuo')
print(all(item in glas for item in s[::2]))