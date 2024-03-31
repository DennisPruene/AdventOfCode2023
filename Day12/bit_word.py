import unittest


class BitWord:
    """A wrapper class for int's to make their use as bit words (sequences of 1s and 0s) clear

    The main use of this class is to directly store the length of a bit word along with the word itself.
    For example the sequences 100 and 000100 can be differientiated by their length alone (3 and 6 respectivelly)
    """

    def __init__(self, word: int, length: int):
        self.word = word
        self.length = length

    def __repr__(self) -> str:
        return f'{self.word:0{self.length}b}'


class TestBitWord(unittest.TestCase):
    def test_repr(self):
        word1 = BitWord(0b100, 3)
        word2 = BitWord(0b100, 6)
        word3 = BitWord(0b01101111, 8)
        self.assertEqual(f'{word1}', '100')
        self.assertEqual(f'{word2}', '000100')
        self.assertEqual(f'{word3}', '01101111')


if __name__ == '__main__':
    unittest.main()
