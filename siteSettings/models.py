from django.db import models

def upload_image_path(instance, filename):
    # print(instance)
    #print(filename)
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
            new_filename=new_filename, 
            final_filename=final_filename
            )

# Create your models here.
class siteSetting (models.Model):
    company         = models.CharField(max_length=120,null=True, blank=True)
    shortCompany    = models.CharField(max_length=60,null=True, blank=True)
    description     = models.TextField()
    crn             = models.CharField(max_length=60,null=True, blank=True)
    vat             = models.CharField(max_length=60,null=True, blank=True)
    address         = models.CharField(max_length=60,null=True, blank=True)
    telephone       = models.CharField(max_length=20,null=True, blank=True)
    fax             = models.CharField(max_length=20,null=True, blank=True)
    website         = models.CharField(max_length=120,null=True, blank=True)
    adminEmail      = models.CharField(max_length=20,null=True, blank=True)
    contactEmail    = models.CharField(max_length=20,null=True, blank=True)
    logo            = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    logo_mini       = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    facebook        = models.CharField(max_length=120,null=True, blank=True)
    twitter        = models.CharField(max_length=120,null=True, blank=True)
    instagram        = models.CharField(max_length=120,null=True, blank=True)
    youtube        = models.CharField(max_length=120,null=True, blank=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company
