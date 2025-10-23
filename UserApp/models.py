from django.db import models
from django.contrib.auth.models import AbstractUser   
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def generate_user_id():
    return "User"+uuid.uuid4().hex[:4].upper()

def verify_email(email):
    domaine=["esprit.tn","sesame.com","tek.tn","central.com"]
    if email.split('@')[-1] not in domaine: #[-1] == last element of the listp
        raise ValidationError("l email est invalide et doit appartenir à un de ces domaines universitaires")

def name_valdiator(name):
    regex=r'^[a-zA-Z\s-]+$' #\s space
    if not RegexValidator(regex)(name):
        raise ValidationError("le nom ne doit contenir que des lettres, des espaces et des tirets")
    
class User(AbstractUser):
    ROLE_CHOICES = [
        ('participant', 'Participant'),
        ('organisateur', 'Organisateur'),
        ('comite', 'Membre du comité scientifique'),
    ]

    user_id=models.CharField(primary_key=True,max_length=8, unique=True,editable=False)
    first_name=models.CharField(max_length=50,validators=[name_valdiator])
    last_name=models.CharField(max_length=50,validators=[name_valdiator])
    affiliation=models.CharField(max_length=100)
    nationality=models.CharField(max_length=50)
    email=models.EmailField(unique=True,validators=[verify_email])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    role=models.CharField(max_length=50,default='participant',choices=ROLE_CHOICES)
    #OrganizingCommittee=models.ManyToManyField("ConferenceApp.Conference", through="OrganizingCommittee")
    #submission=models.ManyToManyField("ConferenceApp.Conference", through="ConferenceApp.Submission")
 
 #-------->   #if you want to work with those manytomany , you need to delete related name from foreign keys   
    
    def __str__(self):
        return self.username
    
    def save(self,*args,**kwargs):
        if not self.user_id:
            new_id = generate_user_id()
            while User.objects.filter(user_id=new_id).exists():
                new_id = generate_user_id()
            self.user_id = new_id
        super().save(*args, **kwargs)
    
class OrganizingCommittee(models.Model):
    roles= [('chair', 'Chair'),
            ('co-chair', 'Co-Chair'),
            ('member', 'Member'),]

    user=models.ForeignKey(User, on_delete=models.CASCADE , related_name="committees" )
    conference=models.ForeignKey("ConferenceApp.conference", on_delete=models.CASCADE , related_name="committees" )    
    committee_role=models.CharField(max_length=100, choices=roles)
    date_joinded=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username
