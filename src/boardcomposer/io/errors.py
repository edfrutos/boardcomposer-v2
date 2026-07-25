"""Errores compartidos por los importadores del Core."""


class LoaderError(ValueError):
    """Un fichero de entrada no puede convertirse en un Project.

    Subclase de ValueError a propósito: los importadores ya dejaban escapar
    ValueError/KeyError en bruto, así que quien los capturara sigue
    funcionando; lo que cambia es que ahora el mensaje dice qué fila y qué
    columna, en vez de una traza de Python delante del usuario del CLI.
    """
