from django.db import models
import re


class UserManager(models.Manager):
    def validator(self, postData):
        
        errors = {}
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must have at least 2 letters."

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must have at least 2 letters."

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"

        email_unique = self.filter(email = postData['email'])
        if email_unique:
            errors['email_unique'] = "Email already in use"
        # try:
        #     # self is the UserManager that has .get method
        #     self.get(email=postData['email'])
        #     errors['email_unique'] = "Email already in use"
        # except:
        #     pass

        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters."

        if postData['password'] != postData['confirm_pw']:
            errors['password_match'] = "Password does not match"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #messages = finds the messages from each user
        # e.g (specific user).messages.all() == list of message objects
        
    #comments = finds the comments from each user
        # e.g this_user.comments.all() == list of all comment objects
    objects = UserManager()


class Message(models.Model):
    content = models.TextField() # content in place of message
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # comments =  finds the comments for each message
        # e.g this_message.comments.all() == list of all comment objects
    objects = UserManager()
    
class Comment(models.Model):
    content = models.TextField()
    user =  models.ForeignKey(User, related_name = "comments", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name = "comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    #{{comment.user.first_name}} 
    #{{comment.message.content}}
    
    
    
