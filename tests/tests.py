import unittest
from app import db
from app.models import Users,Posts,Comments,Subscriptions

class Test(unittest.TestCase):

   def setUp(self):
      self.user_1 = Users(id = 1,name = 'John Doe', username = 'johndoe', email = 'johndoe@email.com', password = 'password')
      self.post_1 = Posts(id = 1,title = "People read this", content = 'This is a test', writer = 1)
      self.comment_1 = Comments(comment = 'Yep! A test.', name = "Jane Doe", posted_on = 1)


   def tearDown(self):
      Users.query.delete()
      Posts.query.delete()
      Comments.query.delete()

   def test_check_instance_variables(self):
        self.assertEquals(self.user_1.name,'John Doe')
        self.assertEquals(self.user_1.email,'johndoe@email.com')
        self.assertEquals(self.post_1.content,"This is a test")
        self.assertEquals(self.post_1.writer,1)
        self.assertEquals(self.comment_1.posted_on,self.post_1.id)