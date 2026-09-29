from app.core.security import get_current_user,require_roles
admin_required=require_roles('admin')
billing_required=require_roles('admin','billing_staff')
