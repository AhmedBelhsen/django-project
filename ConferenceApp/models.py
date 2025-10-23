from datetime import date
import random
import string
from django.db import models
from django.utils import timezone
# Create your models here.
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
class Conference(models.Model):

    def name_conference(name):
        regex=r'^[a-zA-Z\s]+$'
        if not RegexValidator(regex)(name):
            raise ValidationError("le nom de la conférence ne doit contenir que des lettres et des espaces")

    Themechoices =[
        ('Computer Science & Artificial Intelligence', 'Computer Science & Artificial Intelligence'),
        ('Science & Engineering', 'Science & Engineering'),
        ('Social Sciences & Education', 'Social Sciences & Education'),
        ('Interdisciplinary Themes', 'Interdisciplinary Themes'),
    ]
    conference_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,validators=[name_conference])
    theme=models.CharField(max_length=100,choices=Themechoices)
    start_date=models.DateField()
    end_date=models.DateField()
    location=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    description=models.TextField(validators=[MinLengthValidator(limit_value=30,message="la description doit contenir au moins 30 caractères")])

    def __str__(self):
        return self.name
    
    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("la date de fin doit être postérieure à la date de début")

class Submission(models.Model):
    statuschoices =[
        ('submitted', 'Submitted'),
        ('under review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    submission_id=models.CharField(primary_key=True,max_length=8)
    user=models.ForeignKey("UserApp.User", on_delete=models.CASCADE , related_name="submissions" )
    conference=models.ForeignKey(Conference, on_delete=models.CASCADE , related_name="submissions" )
    title=models.CharField(max_length=100)
    abstract=models.TextField()
    keywords=models.CharField(max_length=200)
    paper=models.FileField(upload_to='papers/')
    status=models.CharField(max_length=50,default='submitted',choices=statuschoices)
    submitted_at=models.DateField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    payed=models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):

        if not self.submission_id:
            random_id = ''.join(random.choices(string.ascii_uppercase, k=8))
            self.submission_id = f"SUB-{random_id}"
        super().save(*args, **kwargs)

    def clean(self):
        errors = {}
        if self.conference_id and self.conference_id.start_date < date.today():
            # Change 'conference_id' to 'conference_id' or use __all__ for non-field errors
            errors['conference_id'] = ["La soumission ne peut être faite que pour des conférences à venir."]

        if self.keywords:
            keyword_list = [kw.strip() for kw in self.keywords.split(',') if kw.strip()]
            if len(keyword_list) > 10:
                errors['keywords'] = [f"Vous avez saisi {len(keyword_list)} mots-clés. Le maximum autorisé est 10."]

        if self.user_id:
            today = timezone.now().date()
            today_submissions = Submission.objects.filter(
                user_id=self.user_id,
                submitted_at__date=today
            ).count()
            if not self.pk and today_submissions >= 3:
                errors['user_id'] = ["Vous avez déjà soumis 3 conférences aujourd'hui. Limite journalière atteinte."]

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.submission_id} - {self.title}"
