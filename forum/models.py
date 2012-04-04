from django.db import models
from treebeard.al_tree import AL_Node

class Author(models.Model):
    name = models.CharField(max_length = 200)
    u_id = models.IntegerField()
    gender = models.CharField(max_length = 200)
    posts = models.IntegerField()
    okp_team = models.BooleanField()
    member_since = models.DateTimeField('member since')
    profile_url = models.URLField()
    avatar_url = models.URLField()
    
    def __unicode__(self):
        return self.name
    
class Message(AL_Node):
    mesg_id = models.IntegerField()     # absolute index on forum
    mesg_num = models.IntegerField()    # number displayed to user
    date_time = models.DateTimeField('posting date/time')
    subject = models.CharField(max_length = 200)
    author = models.ForeignKey(Author)
    parent = models.ForeignKey('self',
                               related_name='children_set',
                               null=True,
                               db_index=True)
    node_order_by = ["date_time", "mesg_num", "author"]
    text = models.TextField()
    signature = models.TextField()
    
    def __unicode__(self):
        return self.subject