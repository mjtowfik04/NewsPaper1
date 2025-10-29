from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrReadOnly(BasePermission):
    """
    Staff হলে সব করতে পারবে,
    না হলে শুধু Read-only access পাবে
    """
    def has_permission(self, request, view):
        # যদি GET/HEAD/OPTIONS হয় তাহলে সবাই access পাবে
        if request.method in SAFE_METHODS:
            return True
        
        # Staff হলে সব method এ access পাবে
        return request.user and request.user.is_staff
