from models import db, RolePermission, Permission, UserPermission

def has_permission(user, permission_name):
    role_permissions = db.session.query(RolePermission).join(Permission).filter(
        RolePermission.role == user.role,
        Permission.name == permission_name
    ).all()

    user_permissions = db.session.query(UserPermission).join(Permission).filter(
        UserPermission.user_id == user.user_id,
        Permission.name == permission_name
    ).all()

    return bool(role_permissions or user_permissions)

