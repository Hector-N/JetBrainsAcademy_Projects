import unittest
import regex

class TestRegex(unittest.TestCase):

    def test_char(self):
        self.assertRaises(ValueError, regex.char, 'a', 'aa')
        self.assertRaises(ValueError, regex.char, 'aa', 'a')
        self.assertTrue(regex.char('a', 'a'))
        self.assertTrue(regex.char('.', 'a'))
        self.assertTrue(regex.char('', 'a'))
        self.assertTrue(regex.char('', ''))
        self.assertFalse(regex.char('a', ''))
        self.assertFalse(regex.char('a', 'z'))
        self.assertFalse(regex.char('a', '.'))


    def test_string(self):
        self.assertTrue(regex.string('apple', 'apple'))
        self.assertTrue(regex.string('apple', 'apple'))
        self.assertTrue(regex.string('apple', 'apple'))
        self.assertTrue(regex.string('.pple', 'apple'))
        self.assertTrue(regex.string('appl.', 'apple'))
        self.assertTrue(regex.string('.....', 'apple'))
        self.assertFalse(regex.string('Apple', 'apple'))
        self.assertFalse(regex.string('a', 'b'))

        # stage 5
        self.assertTrue(regex.string('colou?r', 'color'))
        self.assertTrue(regex.string('colou?r', 'colour'))
        self.assertFalse(regex.string('colou?r', 'colouur'))
        self.assertTrue(regex.string('colou*r', 'color'))
        self.assertTrue(regex.string('colou*r', 'colour'))
        self.assertTrue(regex.string('colou*r', 'colouur'))
        self.assertTrue(regex.string('col.*r', 'color'))
        self.assertTrue(regex.string('col.*r', 'colour'))
        self.assertTrue(regex.string('col.*r', 'colr'))
        self.assertTrue(regex.string('col.*r', 'collar'))
        # self.assertFalse(regex.string('col.*r$', 'colors'))  # todo

        # stage 6
        self.assertTrue(regex.string('\\?', '?'))
        # self.assertTrue(regex.string('\\.$', 'end.'))  # todo


        # stage 6
        self.assertTrue(regex.string('\\?', '?'))
        # self.assertTrue(regex.string('\\.$', 'end.'))


    def test_match(self):
        self.assertFalse(regex.match('a', 'b'))
        self.assertFalse(regex.match('^a$', 'b'))
        self.assertTrue(regex.match('a', 'a'))
        self.assertTrue(regex.match('^a$', 'a'))
        self.assertTrue(regex.match('tion', 'tion'))
        self.assertTrue(regex.match('tion', 'question'))
        self.assertTrue(regex.match('tion', 'tion!?'))
        self.assertTrue(regex.match('tion', 'questions?'))
        self.assertTrue(regex.match('.ion', 'sion'))
        self.assertTrue(regex.match('.', 'abracadabra'))
        self.assertFalse(regex.match('tion', 'sion'))
        self.assertTrue(regex.match('', 'sion'))
        self.assertFalse(regex.match('tion', 'tio'))
        self.assertTrue(regex.match('^gui', 'guitarra'))
        self.assertTrue(regex.match('^...', 'guitarra'))
        self.assertFalse(regex.match('^gui', 'Guitarra'))
        self.assertTrue(regex.match('^.ui', 'Guitarra'))
        self.assertFalse(regex.match('^ui', 'Guitarra'))
        self.assertTrue(regex.match('^guitarra$', 'guitarra'))
        self.assertFalse(regex.match('^guitarra$', 'guitarrA'))
        self.assertFalse(regex.match('^guitarra$', 'guitarra2'))
        self.assertFalse(regex.match('^guitarra$', 'Guitarra'))
        self.assertTrue(regex.match('^.uitarra$', 'Guitarra'))
        self.assertFalse(regex.match('^guitarra$', '2guitarra'))
        self.assertFalse(regex.match('^tarra$', 'guitarra'))
        self.assertTrue(regex.match('le$', 'apple'))

        # stage 6
        self.assertTrue(regex.match('\\.$', 'end.'))
        self.assertTrue(regex.match('3\\+3', '3+3=6'))
        self.assertTrue(regex.match('\\?', 'Is this working?'))
        self.assertTrue(regex.match('\\\\', '\\'))
        self.assertFalse(regex.match('colou\\?r', 'color'))
        self.assertFalse(regex.match('colou\\?r', 'colour'))


if __name__ == '__main__':
    unittest.main()
