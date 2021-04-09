from django.db import models

class DepartmentalGroup(models.Model):
    group_code = models.CharField("Group Code", primary_key=True, max_length=6)
    group_name = models.CharField("Group Name", max_length=300)
    def __str__(self):
        return str(self.group_name)

    class Meta:
        verbose_name = "Departmental Group"
        verbose_name_plural = "Departmental Groups"
        ordering = ["group_name"]


class Directorate(models.Model):
    directorate_code = models.CharField(
        "Directorate Code", primary_key=True, max_length=6
    )
    directorate_name = models.CharField("Directorate Name", max_length=300)
    group = models.ForeignKey(DepartmentalGroup, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Directorate"
        verbose_name_plural = "Directorates"
        ordering = ["directorate_name"]


class CostCentre(models.Model):
    cost_centre_code = models.CharField(
        "Cost Centre Code", primary_key=True, max_length=6
    )
    cost_centre_name = models.CharField("Cost Centre Name", max_length=300)
    directorate = models.ForeignKey(Directorate, on_delete=models.PROTECT)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Cost Centre"
        verbose_name_plural = "Cost Centres"
        ordering = ["cost_centre_name"]
