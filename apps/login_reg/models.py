from django.db import models
from django.core.validators import validate_email , RegexValidator
import bcrypt 
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
#  not using regex but here for reference

class UserManager(models.Manager):
    def validateUser(self, postData):
        result = {'errors' :[]}
# check for pw mismatch
        if postData['password'] != postData['confirm_password']:
            result['errors'].append("Passwords do not match")
# handles case where password input is deleted 
        if len(postData['password']) < 8:
            result['errors'].append("Passwords must be 8 or more characters")
# handles case where first_name input is deleted 
        if len(postData['first_name']) < 2:
            result['errors'].append("First Name must be 2 or more characters")            
# handles case where last_name input is deleted 
        if len(postData['last_name']) < 2:
            result['errors'].append("Last Name must be 2 or more characters")
        try:
            if postData['last_name'].isalpha() ==False or postData['first_name'].isalpha() ==False:
                result['errors'].append("Name fields can only be english letters")
        except:
            pass
# EMAIL
        try:
            validate_email(postData['email'])
        except:
            result['errors'].append("Invalid email")
# escape function if errors exist
        if len(result['errors']) > 0:
            print("errors found, escaping now...")
            return result
        else:
            print("User create pass")
#  LAST THING HERE CHECK IF EMAIL EXISTS in DB  
            throwaway =  User.objects.filter(email = postData['email'])
            if len(throwaway) > 0:
                result['errors'].append("Please use another email")
                return result
            hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            hash1 = hash1.decode()
            newUser = User.objects.create(
                first_name=postData['first_name'] , 
                last_name=postData['last_name'],
                email = postData['email'],
                password = hash1
                )
            result['user_id'] = newUser.id
            print(result['user_id'])
            return result

    def LoginValidator(self, postData):
        result = {'errors' :[]}
        throwaway =  User.objects.filter(email = postData['email'])
        if len(throwaway) == 0:
            result['errors'].append("User or Password incorrect")
            return result
        else:
            if bcrypt.checkpw(postData['password'].encode(),throwaway[0].password.encode()):
                result['user_id'] = throwaway[0].id
                return result
            result['errors'].append("User or Password incorrect")
            return result


class User(models.Model):
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    email = models.CharField(max_length= 255)
    password = models.CharField(max_length= 255)
    objects = UserManager()