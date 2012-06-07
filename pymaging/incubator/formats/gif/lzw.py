# -*- coding: utf-8 -*-
from pymaging.utils import bitstruct
import array
import struct

class StringTable(object):
    def __init__(self):
        self.index_to_data = {}
        self.data_to_index = {}
        self.current_index = 0
        
    def push(self, data):
        self.index_to_data[self.current_index] = data
        self.data_to_index[data] = self.current_index
        self.current_index += 1
        
    def get_by_index(self, index):
        return self.index_to_data[index]
    
    def get_by_data(self, data):
        return self.data_to_index[data]

    def check_data(self, data):
        try:
            self.get_by_data(data)
            return True
        except KeyError:
            return False
    
    def check_index(self, index):
        try:
            self.get_by_index(index)
            return True
        except KeyError:
            return False

def compress(data, roots):
    data = list(data)
    roots = list(roots)
    codes = []
#     [1] Initialize string table;
    stringtable = StringTable()
    for root in roots:
        stringtable.push(root)
#     [2] [.c.] <- empty;
    current_prefix = ''
#     [3] K <- next character in charstream;
    for current in data:
#     [4] Is [.c.]K in string table?
        if stringtable.check_data(current_prefix + current):
#      (yes: [.c.] <- [.c.]K;
            current_prefix += current
#            go to [3];
#      )
        else:
#      (no: add [.c.]K to the string table;
            stringtable.push(current_prefix + current)
#           output the code for [.c.] to the codestream;
            codes.append(stringtable.get_by_data(current_prefix))
#           [.c.] <- K;
            current_prefix = current
#           go to [3];
#      )
    codes.append(stringtable.get_by_data(current_prefix))
    return codes

def decompress(codes, roots):
    codes = list(codes)
    roots = list(roots)
    data = []
#     [1] Initialize string table;
    stringtable = StringTable()
    for root in roots:
        stringtable.push(root)
#     [2] get first code: <code>;
    code = codes.pop(0)
#     [3] output the string for <code> to the charstream;
    data.append(stringtable.get_by_index(code))
#     [4] <old> = <code>;
    old = code
#     [5] <code> <- next code in codestream;
    for code in codes:
#     [6] does <code> exist in the string table?
        if stringtable.check_index(code):
#      (yes: output the string for <code> to the charstream;
            data.append(stringtable.get_by_index(code))
#            [...] <- translation for <old>;
            prefix = stringtable.get_by_index(old)
#            K <- first character of translation for <code>;
            K = stringtable.get_by_index(code)[0]
#            add [...]K to the string table;
            stringtable.push(prefix + K)
#            <old> <- <code>;
            old = code
#      )
        else:
#      (no: [...] <- translation for <old>;
            prefix = stringtable.get_by_index(old)
#           K <- first character of [...];
            K = prefix[0]
#           output [...]K to charstream and add it to string table;
            data.append(prefix + K)
            stringtable.push(prefix + K)
#           <old> <- <code>
            old = code
#      )
#     [7] go to [5];
    return data


def get_bits(fileobj, eoi):
    while True:
        block_size = struct.unpack('<B', fileobj.read(1))[0]
        data = struct.unpack('<%sB' % block_size, fileobj.read(block_size))
        for byte in data:
            print(byte)
            if byte == eoi:
                raise StopIteration()
            for bit in bitstruct((1,1,1,1,1,1,1,1), byte):
                yield bit

class GifLZWDecompressor(object):
    def __init__(self, fileobj, code_size, line_length):
        self.fileobj = fileobj
        self.code_size = code_size
        n = max(2, code_size)
        self.root_size = (2 ** n) - 1
        self.clear_code = 2 ** n
        self.compression_size = n + 1
        self.end_of_input = self.clear_code + 1
        self.line_length = line_length
        self.bititer = get_bits(self.fileobj, self.end_of_input)
        self.init_stringtable()
        
    def init_stringtable(self):
        self.stringtable = StringTable()
        for i in range(self.root_size):
            self.stringtable.push(i)
        self.stringtable.push(self.clear_code)
        self.stringtable.push(self.end_of_input)
        print(self.stringtable.index_to_data)
        
    def bump(self):
        self.compression_size += 1
        self.init_stringtable()
    
    def get_code(self):
        s = ''
        for _ in range(self.compression_size):
            s += str(next(self.bititer))
        return int(s, 2)
    
    def _decompress_data(self):
        print(list(self.bititer))
        code = self.get_code()
        yield self.stringtable.get_by_index(code)
        old = code
        while True:
            code = self.get_code()
            if code is None:
                break
            if self.stringtable.check_index(code):
                yield self.stringtable.get_by_index(code)
                prefix = self.stringtable.get_by_index(old)
                K = self.stringtable.get_by_index(code)[0]
                self.stringtable.push(prefix + K)
                old = code
            else:
                prefix = self.stringtable.get_by_index(old)
                K = prefix[0]
                yield prefix + K
                self.stringtable.push(prefix + K)
                old = code

    def decompress(self):
        #expectation: 2,3,1,0
        lines = []
        current_line = array.array('B')
        for data in self._decompress_data():
            current_line.append(data)
            if len(current_line) == self.line_length:
                lines.append(current_line)
                current_line = array.array('B')
        return lines
