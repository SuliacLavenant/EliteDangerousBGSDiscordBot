class AbstractPermissions:
    super_admin_id: int | None = None

    @classmethod
    def set_super_admin_id(cls, user_id):
        cls.super_admin_id = user_id

    @classmethod
    def is_user_super_admin(cls, user_id: int) -> bool:
        return cls.super_admin_id is not None and cls.super_admin_id == user_id