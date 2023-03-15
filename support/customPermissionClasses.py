from rest_framework import permissions


def users_all_permission(request):
    permissions = []
    permissions_codename = []
    user_permissions = request.user.user_permissions.all()
    all_group = request.user.groups.all()
    for grp in all_group:
        grp_permissions = grp.permissions.all()
        for perm in grp_permissions:
            permissions.append(perm)

    for perm in user_permissions:
        permissions.append(perm)

    permissions = list(set(permissions))

    for permission in permissions:
        permissions_codename.append(permission.codename)

    return permissions_codename


class CustomPermissionsCheck(permissions.BasePermission):

    def has_permission(self, request, view):
        from_view = view.get_view_name()
        # print('from_view',from_view)
        permissions_codename = users_all_permission(request)
        if (request.user.is_authenticated):
            if (from_view=='Invoice Payment' and ("add_invoice_payment" in permissions_codename)):
                return True
            elif (from_view=='General Ledger' and ("view_general_ledger" in permissions_codename)):
                return True
            elif (from_view=='Client Balance' and ("view_client_balance" in permissions_codename)):
                return True
            elif (from_view=='Dashboard Summary' and ("dashboard_summary" in permissions_codename)):
                return True
        return False