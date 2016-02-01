from django.db import models


class CertificateAuthority(models.Model):
    revoked = models.BooleanField(default=False)
    key = models.TextField()
    crt = models.TextField()
    next_serial = models.IntegerField(default=1)
    date_created = models.DateTimeField()

class Certificate(models.Model):
    revoked = models.BooleanField(default=False)
    key = models.TextField()
    crt = models.TextField()
    ca = models.ForeignKey(CertificateAuthority)
    date_created = models.DateTimeField()
    md5 = models.CharField(max_length=20)
    serial = models.IntegerField()
    device = models.ForeignKey("mdm.device", blank=True, null=True)

