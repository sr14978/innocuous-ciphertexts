
def pad(input, block_size):
    input += '1'
    length = len(input)
    mod = length % block_size
    if mod != 0:
        input += '0'*(block_size-mod)
    return inputs

def unpad(input):
    while input[-1] != '1':
        input = input[:-1]
    return input
