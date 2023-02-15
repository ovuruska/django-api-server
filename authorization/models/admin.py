from scheduling.models import Employee


class AdminAuth(Employee):
    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'
