from django.db import models
from ..login.models import User
import datetime

class DestinationManager(models.Manager):
    def validate_destination(self, post_data, date, user_id):
        result = {
            'status': False
        }
        errors = []
        if len(post_data['destination']) <1:
            errors.append('Valid input requres a destination')
        if len(post_data['description']) <1:
            errors.append('You must say what you will do when you reach your destination.')
        if post_data['startdate'] < date:
            errors.append('Start date for plans cannot be set in the past.')
        if post_data['enddate'] < post_data['startdate']:
            errors.append('Conclusion date predates the start time.')

        if len(errors) >0:
            result['errors'] = errors
        else:
            result['status'] = True
            new_travelplan = Destination.objects.create(
                creator = User.objects.get(id=user_id),
                destination = post_data['destination'],
                description = post_data['description'],
                startdate = post_data['startdate'],
                enddate = post_data['enddate']
            )
            new_travelplan.joiners.add(User.objects.get(id=user_id))
            new_travelplan.save()
            print('Travel plan has been logged')
        return result



class Destination(models.Model):
    creator = models.ForeignKey(User, related_name="trip_host")
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField()
    joiners = models.ManyToManyField(User, related_name="participants_joined")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DestinationManager()
    def __repr__(self):
        return "id = {}, creator = {}, destination = {}, description = {}".format(self.id, self.creator, self.destination, self.description)

