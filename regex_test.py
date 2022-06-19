import unittest

from regex import *
import logging


# use AOP to check the input
def AOPCheckInput(regex:Regex,pattern: str) -> bool:
    if len(pattern) == 0:
        logging.info('pattern can not be empty')
        return False
    if pattern[0] in ['*', '+']:
        logging.info('* + can not exist in this position')
        return False
    if pattern.count('[') != pattern.count(']'):
        logging.info('[ ] must exist in pair')
        return False
    if pattern.count('{') != pattern.count('}'):
        logging.info('{ } must exist in pair')
        return False

    regex.compile(pattern)
    return True

class TestMutable(unittest.TestCase):

    def test_error_input(self):
        regex = Regex()
        self.assertEqual(AOPCheckInput(regex, '*aa'), False)
        self.assertEqual(AOPCheckInput(regex, '+ba'), False)
        self.assertEqual(AOPCheckInput(regex, '[1,q12re'), False)
        self.assertEqual(AOPCheckInput(regex, '1,q12re,3}'), False)

    def test_star(self):
        regex = Regex()
        # test match
        AOPCheckInput(regex,'a*')
        #regex.compile('a*')
        self.assertEqual(regex.match('aaaaa'), (0,5))
        AOPCheckInput(regex,'a*bbbc')
        self.assertEqual(regex.match('aaaaabbbc'), (0,9))
        AOPCheckInput(regex,'a*bbbc')
        self.assertEqual(regex.match('bbbc'), (0,4))
        AOPCheckInput(regex,'a*bbbc')
        self.assertEqual(regex.match('cbbbc'), None)
        # test search
        AOPCheckInput(regex,'a*')
        self.assertEqual(regex.search('baaa'), (1,4))
        AOPCheckInput(regex,'a*bbbc')
        self.assertEqual(regex.search('aaaaabbbc'), (0,9))
        AOPCheckInput(regex,'a*bbbc')
        self.assertEqual(regex.search('xxxbbbc'), (3,7))

    def test_plus(self):
        regex = Regex()
        # test match
        AOPCheckInput(regex,'a+')
        self.assertEqual(regex.match('aaaaa'), (0,5))
        AOPCheckInput(regex,'a+')
        self.assertEqual(regex.match('sadw'), None)
        AOPCheckInput(regex,'a+bbb')
        self.assertEqual(regex.match('aaabbb'), (0,6))
        # test search
        AOPCheckInput(regex,'a+bbb')
        self.assertEqual(regex.search('aaabbb'), (0,6))
        AOPCheckInput(regex,'a+bb')
        self.assertEqual(regex.search('xxxaaabb'), (3,8))

    def test_dot(self):
        regex = Regex()
        # test match
        AOPCheckInput(regex,'a.')
        self.assertEqual(regex.match('aa'), (0,2))
        AOPCheckInput(regex,'a...cef')
        self.assertEqual(regex.match('a123cef'), (0,7))
        AOPCheckInput(regex,'a...cef')
        self.assertEqual(regex.match('x123cef'), None)
        # test search
        AOPCheckInput(regex,'a.')
        self.assertEqual(regex.search('xxaa'), (2,4))
        AOPCheckInput(regex,'a..xx.')
        self.assertEqual(regex.search('xxaa8xx9'), (2,8))
        AOPCheckInput(regex,'a..xx.')
        self.assertEqual(regex.search('xxaa87x9'), None)

    def test_digital(self):
        regex = Regex()
        # test match
        AOPCheckInput(regex,'\\d\\d')
        self.assertEqual(regex.match('22'), (0,2))
        AOPCheckInput(regex,'a\\de')
        self.assertEqual(regex.match('a8e'), (0,3))
        # test search
        AOPCheckInput(regex,'a\\de')
        self.assertEqual(regex.search('xxa8e'), (2,5))
        AOPCheckInput(regex,'\\d')
        self.assertEqual(regex.search('xxa8e'), (3,4))

    def test_space(self):
        regex = Regex()
        # test match
        AOPCheckInput(regex,'abc\\s\\s')
        self.assertEqual(regex.match('abc  '), (0,5))
        AOPCheckInput(regex,'\\sefc')
        self.assertEqual(regex.match(' efc'), (0,4))
        AOPCheckInput(regex,'\\sefc')
        self.assertEqual(regex.match('efc'), None)
        # test search
        AOPCheckInput(regex,'\\sefc')
        self.assertEqual(regex.search('efc'), None)
        AOPCheckInput(regex,'\\sefc')
        self.assertEqual(regex.search('abcd efc'), (4,8))

    def test_character(self):
        regex = Regex()
        # test match
        AOPCheckInput(regex,'\\w\\wb')
        self.assertEqual(regex.match('1ab'), (0,3))
        AOPCheckInput(regex,'\\w\\wb')
        self.assertEqual(regex.match('1ac'), None)
        # test search
        AOPCheckInput(regex,'\\w\\wb')
        self.assertEqual(regex.search('1ab'), (0,3))
        AOPCheckInput(regex,'\\w\\wb')
        self.assertEqual(regex.search('xx1ab'), (2,5))

    def test_diagonal(self):
        regex = Regex()
        # test match
        AOPCheckInput(regex,'\\n')
        self.assertEqual(regex.match('n'), (0,1))
        AOPCheckInput(regex,'\\n')
        self.assertEqual(regex.match('x'), None)
        # test search
        AOPCheckInput(regex,'\\o')
        self.assertEqual(regex.search('abcdeo'), (5,6))
        AOPCheckInput(regex,'\\n')
        self.assertEqual(regex.search('abcde1234'), None)

    def test_hat(self):
        regex = Regex()
        # test match
        AOPCheckInput(regex,'^abcd')
        self.assertEqual(regex.match('abcddd'), (0,4))
        AOPCheckInput(regex,'^abcd')
        self.assertEqual(regex.match('xabcddd'), None)
        # test search
        AOPCheckInput(regex,'^abcd')
        self.assertEqual(regex.search('abcddd'), (0,4))
        AOPCheckInput(regex,'^abcd')
        self.assertEqual(regex.search('xxxabcddd'), None)

    def test_doller(self):
        regex = Regex()
        # test match
        AOPCheckInput(regex,'abcd$')
        self.assertEqual(regex.match('abacdddabcd'), (7,11))
        AOPCheckInput(regex,'abcd$')
        self.assertEqual(regex.match('abacdddabcdx'), None)
        # test search
        AOPCheckInput(regex,'abcd$')
        self.assertEqual(regex.search('abacdddabcdx'), None)
        AOPCheckInput(regex,'abcd$')
        self.assertEqual(regex.search('qweabacdddabcd'), (10,14))

    def test_rect(self):
        regex = Regex()
        # test match
        AOPCheckInput(regex,'[abc]')
        self.assertEqual(regex.match('dhgeardhrty'), None)
        AOPCheckInput(regex,'[abc]')
        self.assertEqual(regex.match('kbkk'), None)
        AOPCheckInput(regex,'[abc]')
        self.assertEqual(regex.match('abccqweeryt'), (0,1))
        # test search
        AOPCheckInput(regex,'[abc]')
        self.assertEqual(regex.search('xxxabccqweeryt'), (3,4))
        AOPCheckInput(regex,'[anc]')
        self.assertEqual(regex.search('xxxqweeryt'), None)

    # test [^]
    def test_hatRect(self):
        regex = Regex()
        # text match
        AOPCheckInput(regex,'[^abc]')
        self.assertEqual(regex.match('abc'), None)
        AOPCheckInput(regex,'[^abc]')
        self.assertEqual(regex.match('kkk'), (0,1))
        AOPCheckInput(regex,'[^abc]')
        self.assertEqual(regex.match('adwerx'), None)
        # text search
        AOPCheckInput(regex,'[^abc]')
        self.assertEqual(regex.match('abc'), None)
        AOPCheckInput(regex,'[^abc]')
        self.assertEqual(regex.match('mabc'), (0,1))

    # test {n}
    def test_repeat_n(self):
        regex = Regex()
        # text match
        AOPCheckInput(regex,'a{3}')
        self.assertEqual(regex.match('aaaaaa'), (0,3))
        AOPCheckInput(regex,'a{3}')
        self.assertEqual(regex.match('xxaaaaaa'), None)
        # test search
        AOPCheckInput(regex,'a{3}')
        self.assertEqual(regex.search('xxaaaxxx'),(2,5))
        AOPCheckInput(regex,'a{3}')
        self.assertEqual(regex.search('xxaaxxx'),None)

    # test {n,} {,m} {n,m}
    def test_repeat_n_m(self):
        regex = Regex()
        # text match
        # 1. test {n,}
        AOPCheckInput(regex,'a{3,}')
        self.assertEqual(regex.match('aaaaaa'), (0,6))
        AOPCheckInput(regex,'a{3,}')
        self.assertEqual(regex.match('aa'), None)
        # 2. test {,m}
        AOPCheckInput(regex,'a{,3}')
        self.assertEqual(regex.match('aaaaaa'), (0,3))
        AOPCheckInput(regex,'a{,3}')
        self.assertEqual(regex.match('aa'), (0,2))
        AOPCheckInput(regex,'a{,3}')
        self.assertEqual(regex.match('caacadas'), (0,0))
        # 3. test {n,m}
        AOPCheckInput(regex,'a{1,3}')
        self.assertEqual(regex.match('a'), (0,1))
        AOPCheckInput(regex,'a{1,3}')
        self.assertEqual(regex.match('aaa'), (0,3))
        AOPCheckInput(regex,'a{1,3}')
        self.assertEqual(regex.match('aaaaaa'), (0,3))
        AOPCheckInput(regex,'a{3,5}')
        self.assertEqual(regex.match('aa'), None)

        # test search
        # 1. test {n,}
        AOPCheckInput(regex,'a{3,}')
        self.assertEqual(regex.search('xaaaaaa'), (1,7))
        AOPCheckInput(regex,'k{2,}')
        self.assertEqual(regex.search('xaakka'), (3,5))
        # 2. test {,m}
        AOPCheckInput(regex,'k{,3}')
        self.assertEqual(regex.search('akkka'), (1,4))
        AOPCheckInput(regex,'k{,3}')
        self.assertEqual(regex.search('akkkkkkkka'), (1,4))
        AOPCheckInput(regex,'k{,3}')
        self.assertEqual(regex.search('aqwetrety'), (0,0))
        # 3. test {n,m}
        AOPCheckInput(regex,'k{1,3}')
        self.assertEqual(regex.search('akkkkkkkaaa'), (1,4))
        AOPCheckInput(regex,'k{3,8}')
        self.assertEqual(regex.search('aakkczxczx'), None)

    def test_sub(self):
        regex = Regex()
        self.assertEqual(regex.sub('aaa','CPO','xxxaaa123456789'),'xxxCPO123456789')
        self.assertEqual(regex.sub('aaa','CPO','xxxwww123456789'),'xxxwww123456789')
        self.assertEqual(regex.sub('aaa','CPO','xxxaaa1234aaa8aa9',count=2),'xxxCPO1234CPO8aa9')
        self.assertEqual(regex.sub('\\d\\d', 'CPO', 'xxxaaa1234aaa89', count=3), 'xxxaaaCPOCPOaaaCPO')

    def test_split(self):
        regex = Regex()
        self.assertEqual(regex.split('x','aaaxaaaxaaa'),['aaa', 'aaa', 'aaa'])
        self.assertEqual(regex.split('x','axxxa'),['a', '', '', 'a'])
        self.assertEqual(regex.split('x','aa'),['aa'])
        self.assertEqual(regex.split('\\d\\d','a12134a'),['a', '', '4a'])

    def test_visual(self):
        regex = Regex()
        AOPCheckInput(regex,'a\\de')
        regex.visualize('pic1')
        AOPCheckInput(regex,'a{2,5}')
        regex.visualize('pic2')
        AOPCheckInput(regex,'abcd$')
        regex.visualize('pic3')
        AOPCheckInput(regex,'[abc]')
        regex.visualize('pic4')
        AOPCheckInput(regex,'a*bbbc')
        regex.visualize('pic5')

    def test_complex_example(self):
        regex = Regex()
        # case 1
        AOPCheckInput(regex,'a*x..yz{2}z')
        self.assertEqual(regex.match("aaaax12yzzz"),(0,11))
        self.assertEqual(regex.match("ax12yzzz"),(0,8))
        self.assertEqual(regex.match("x12yzzz"),(0,7))
        # case 2
        AOPCheckInput(regex,'\\d\\d\\d\\d-\\d\\d-\\d\\d')
        self.assertEqual(regex.search('i am born in 2020-10-19'),(13,23))
        # case 3
        # before : AOPCheckInput(regex,'\\d+@qq\....')
        AOPCheckInput(regex,'\\d+@qq\\....')
        self.assertEqual(regex.match('442653227@qq.com'),(0,16))
        self.assertEqual(regex.search('{"people":[{"name":"niyijie","email":"442653227@qq.com"},{"firstName":"sunqing","lastName":"326299717@qq.com"}]}'),(38,54))
        AOPCheckInput(regex,'su.+g')
        self.assertEqual(regex.search('{"people":[{"name":"niyijie","email":"442653227@qq.com"},{"firstName":"sunqing","lastName":"326299717@qq.com"}]}'),(71,78))

if __name__ == '__main__':
    unittest.main()
