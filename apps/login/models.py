from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_registration(self, post_data, date):
        result = {                                  #creates result object
            'status' : False                        #result object has status boolean set to false
        }
        errors = []                                 #establish error array for validation
        if len(post_data['name']) <3:
            errors.append('Name is not long enough')
        if len(post_data['alias']) <3:
            errors.append('Alias is not long enough')
        if not EMAIL_REGEX.match(post_data['email']):
            errors.append('Email address is not valid')
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append('Email is in use')
        if len(post_data['password']) <8:
            errors.append('Password is not long enough')
        if post_data['password'] != post_data['confirm_pw']:
            errors.append('Passwords do not match')
        if post_data['bday'] >= date:
            errors.append('Birthdate cannot be in the future or current day.')

        if len(errors) >0:
            result['errors'] = errors
        else:
            hashed = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt())

            new_user = User.objects.create(
                name = post_data['name'],
                alias = post_data['alias'],
                email = post_data['email'],
                bday = post_data['bday'],
                password = hashed
            )
            result['name'] = new_user.name
            result['user_id'] = new_user.id 
            result['status'] = True
        return result

    def validate_login(self, post_data):
        result = {                                  #creates result object
            'status' : False                        #result object has status boolean set to false
        }
        errors = []                                 #establish error array for validation
        existing = User.objects.filter(email=post_data['email'])
        if len(existing) < 1:
            errors.append('Email not registered.')
        else:
            if not bcrypt.checkpw(post_data['password'].encode(), existing[0].password.encode()):
                errors.append('Invalid password.')
            else:
                result['user_id'] = existing[0].id
        if len(errors) > 0:
            result['errors'] = errors
        else:
            result['name'] = existing[0].name
            result['status'] = True
        return result

class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    bday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "name = {}, id = {}, email = {}".format(self.name, self.id, self.email)