from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class CustomUserAccessRequiredMixin(AccessMixin):
    """
    Custom AccessMixin to check if user is superuser and active
    status is true
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_active or not request.user.is_superuser:
            # return self.handle_no_permission()
            return redirect("maintenance_dashboard")
        return super().dispatch(request, *args, **kwargs)  # type: ignore
