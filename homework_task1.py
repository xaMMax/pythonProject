yourStr = input('Please type your string here ') # input sample string
if len(yourStr) >= 2:                            # use function len for compare and
    expString = yourStr[:2] + yourStr[-2:]
    print('your string is ' + yourStr, 'and expected result is ' + expString)
else: print('empty string')
