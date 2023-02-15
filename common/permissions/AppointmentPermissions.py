from rest_framework.permissions import BasePermission

from common.extract_role import extract_role
from common.roles import Roles


class CanCreateAppointment(BasePermission):

    @extract_role
    def has_permission(self, request, view):
        return request.user.role >= Roles.CUSTOMER # >= olmayacak mı?


class CanUpdateAppointment(BasePermission):

    @extract_role
    def has_permission(self, request, view):
        return request.user.role >= Roles.CUSTOMER

class CanAppointmentEmployeeRetrieve(BasePermission):

    @extract_role
    def has_permission(self, request, view):
        return request.user.role >= Roles.EMPLOYEE_WE_WASH