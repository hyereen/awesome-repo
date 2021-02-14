from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, room): # room이 obj
        # 여기서 obj는 room을 의미
        return room.user == request.user