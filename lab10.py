import unittest
from parameterized import parameterized
from unittest.mock import Mock


# class MathTool:
#     def add(self, a, b):
#         return a + b
#
#     def subs(self, a, b):
#         return a - b
#
#     def mult(self, a, b):
#         return a * b
#
#     def divide(self, a, b):
#         return a/b
#
# class TestMathTool(unittest.TestCase):
#     def setUp(self):
#         self.calc = MathTool()
#
#     def test_add(self):
#         self.assertEqual(self.calc.add(1, 1), 2)
#         self.assertEqual(self.calc.add(1, 2), 3)
#         self.assertEqual(self.calc.add(4, 3), 7)
#
#     def test_subs(self):
#         self.assertEqual(self.calc.subs(10, 5), 5)
#         self.assertEqual(self.calc.subs(5,10), -5)
#         self.assertEqual(self.calc.subs(0,0),0)
#
#     def test_mult(self):
#         self.assertEqual(self.calc.mult(3,5),15)
#         self.assertEqual(self.calc.mult(1,1),1)
#         self.assertEqual(self.calc.mult(8,8),64)
#
#     def test_divide(self):
#         self.assertEqual(self.calc.divide(9,3),3)
#         self.assertEqual(self.calc.divide(50,10),5)
#
#         with self.assertRaises(ZeroDivisionError):
#                 self.calc.divide(5,0)
#
#
# if __name__ == '__main__':
#     unittest.main()



# class LibraryItem:
#     def __init__(self, title, author, year):
#         self.title = title
#         self.author = author
#         self.year = year
#
#     def details(self):
#         return f"Книга: '{self.title}', Автор: {self.author}, Рік видання: {self.year}"
#
# class TestLibraryItem(unittest.TestCase):
#     def test_details(self):
#         item1 = LibraryItem("Як Україна втрачала Донбас", "Денис Казанський, Марина Воротинцева", 2020)
#         item2 = LibraryItem("1984", "Джордж Орвелл", 1949)
#
#         self.assertEqual(item1.details(),
#             "Книга: 'Як Україна втрачала Донбас', Автор: Денис Казанський, Марина Воротинцева, Рік видання: 2020")
#         self.assertEqual(item2.details(),"Книга: '1984', Автор: Джордж Орвелл, Рік видання: 1949")


#
#
# class NotificationService:
#     def send(self, user, message):
#         pass
#
# class UserManager:
#     def __init__(self, notification_service):
#         self.notification_service = notification_service
#
#     def notify_user(self, user, message):
#         self.notification_service.send(user, message)
#
#
# class TestUserManager(unittest.TestCase):
#     def test_notify_user(self):
#         mock_service = Mock(spec=NotificationService)
#         manager = UserManager(mock_service)
#         manager.notify_user("Oleh", "Hello!")
#         mock_service.send.assert_called_once_with("Oleh", "Hello!")



def check_even(number):
    if number %2 == 0:
        return True
    else:
        return False

class TestEvenNumber(unittest.TestCase):
    @parameterized.expand([
        ("positive_even", 4, True),
        ("positive_odd", 3, False),
        ("negative_even", -2, True),
        ("negative_odd", -7, False),
        ("zero", 0, True),
    ])

    def test_check_even(self, number, val, expected):
        self.assertEqual(check_even(val), expected)

if __name__ == '__main__':
    unittest.main()