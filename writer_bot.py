import sys
from random import seed, randint
SEED = 8
seed(SEED)
NONWORD = '@'

'''
Purpose: This program generates random text based on a source file
         using a Markov Chain algorithm and a custom Hash Table ADT.
         It uses a specified prefix size and generates a desired number
         of words, while handling collisions with linear probing.
'''


class Hashtable:
    '''
    A hash table implementation with linear probing for collision handling.

    Attributes:
        _pairs (list): The underlying list to store key-value pairs.
        _size (int): The size of the hash table.
    '''
    def __init__(self, size):
        '''Initializes the hash table with a given size.'''
        self._pairs = [None] * size
        self._size = size

    def _hash(self, key):
        '''
            Hashes a key into an integer and determines 
            the hash value of the string
            Parameters: key
            Returns:
                the hash value of the key
        '''
        p = 0
        for c in key:
            p = 31 * p + ord(c)
        return p % self._size

    def put(self, key, value):
        '''
        Inserts a key and value into the hash table using linear probing.

        Parameters:
            key (str): The key to insert into the hash table.
            value (any): The value associated with the key.

        Returns:
            None
        '''
        i = self._hash(key)
        if self._pairs[i] != None:
            while True:
                i -= 1 
                if i < 0:
                    i = len(self._pairs) - 1 
                if self._pairs[i] == None:
                    break
        self._pairs[i] = [key, [value]]

    def get(self, key):
        '''
        Retrieves the value list associated with the given key,
        or None if the key is not found.
        Args:
            key: The key whose associated value list is to be retrieved.

            The value list associated with the given key, 
            or None if the key is not found.
        Returns:
            the key or none if the key is not found
        '''
        i = self._hash(key)
        start = i
        while self._pairs[i] is not None:
            if self._pairs[i][0] == key:
                return self._pairs[i][1]
            i = (i - 1) % self._size
            if i == start:
                break
        return None

    def __contains__(self, key):
        '''Checks if a key exists in the hash table.

            Returns:
                Bool: True if key exists, else false
        '''
        if self.get(key) is None:
            return False
        return True

    def __str__(self):
        '''Returns a string representation of the hash table.

            Returns:
                str: the hashtable list as a string
        '''
        return str(self._pairs)

def read_file(filename):
    '''
    Reads the content of a file and returns all words in a list.

    Parameters:
        filename (str): The name of the input file.

    Returns:
        content (list): A list of words from the file.
    '''
    info = open(filename, 'r')
    content = []
    for line in info:
        line = line.strip().split()
        for words in line:
            content.append(words)
    info.close()
    return content

def build_prefix_suffix_table(contents, n, table_size):
    '''
    Builds the prefix-suffix hash table from the contents.

    Parameters:
        contents (list): A list of words from the input file.
        n (int): The prefix size (number of words in a prefix).
        table_size (int): The size of the hash table.

    Returns:
        Hashtable: The populated hash table containing prefixes as keys
                   and lists of possible suffixes as values.
    '''
    table = Hashtable(table_size)
    prefix = [NONWORD] * n
    for word in contents:
        prefix_str = ' '.join(prefix)
        if prefix_str in table:
            table.get(prefix_str).append(word)
        else:
            table.put(prefix_str, word)
        prefix.pop(0)
        prefix.append(word)
    return table

def generate_text(table, n, word_count):
    '''
    Generates a list of words using a prefix-suffix hash table.
    The process starts with a NONWORD prefix and 
    randomly selects a suffix
    Parameters:
        table (hastable): A prefix-suffix hash table.
         n (int): The prefix size.
        word_count (int): Number of words to generate.
    Returns:
        tlist (list): the generated words list
    '''

    tlist = []
    prefix = [NONWORD] * n
    prefix_str = ' '.join(prefix)
    while prefix_str in table and len(tlist) < word_count:
        suffixes = table.get(prefix_str)
        if len(suffixes) > 1:
            i = randint(0, len(suffixes) - 1)
            right_word = suffixes[i]
        else:
            right_word = suffixes[0]
        tlist.append(right_word)
        prefix.pop(0)
        prefix.append(right_word)
        prefix_str = ' '.join(prefix)
    return tlist

def main():
    """
    Main function to execute the program that processes user input,
    builds the table, generates the text, and prints it.
    """
    filename = input()
    table_size = int(input())
    prefix_size = int(input())
    word_count = int(input())

    if prefix_size < 1:
        print("ERROR: specified prefix size is less than one")
        sys.exit(0)
    if word_count < 1:
        print("ERROR: specified size of the generated text is less than one")
        sys.exit(0)

    contents = read_file(filename)
    table = build_prefix_suffix_table(contents, prefix_size, table_size)
    text_generated = generate_text(table, prefix_size, word_count)

    for i in range(0, len(text_generated), 10):
        print(' '.join(text_generated[i:i+10]))

main()
