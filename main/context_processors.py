def avatar_mtime(request):
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.avatar:
        try:
            mtime = int(request.user.profile.avatar.file.storage.get_modified_time(request.user.profile.avatar).timestamp())
        except Exception:
            mtime = 0
        return {'avatar_mtime': mtime}
    return {'avatar_mtime': 0} 