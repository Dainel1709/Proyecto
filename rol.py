def requiere_rol(*roles_permitidos):
    def decorador(func):
        def wrapper(usuario_actual, *args, **kwargs):
            # La directora siempre tiene acceso a todo
            if usuario_actual.rol not in roles_permitidos and usuario_actual.rol != 'Directora':
                raise PermissionError(f"Acceso denegado. Esta acción requiere ser: {', '.join(roles_permitidos)}.")
            return func(usuario_actual, *args, **kwargs)
        return wrapper
    return decorador