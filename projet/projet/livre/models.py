from django.db import models

# Create your models here.

class Livre(models.Model):  
    idLivre = models.IntegerField(primary_key=True)
    titre = models.CharField(max_length=300)  
    auteur = models.CharField(max_length=300)
    lien = models.CharField(max_length=300)


class Mot(models.Model):
    mot = models.CharField(max_length=100)

class Index(models.Model):
    idLivre = models.ForeignKey(Livre, on_delete=models.CASCADE, blank=True, null=True)
    idMot = models.ForeignKey(Mot, on_delete=models.CASCADE, blank=True, null=True)
    nbOccurrence = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['idLivre', 'idMot'], name='unique_migration_host_combination'
            )
        ]

class Jaccard(models.Model):
    idLivre1 = models.ForeignKey(Livre, on_delete=models.CASCADE, blank=True, null=True, related_name='l1')
    idLivre2 = models.ForeignKey(Livre, on_delete=models.CASCADE, blank=True, null=True, related_name='l2')
    distance = models.IntegerField()

