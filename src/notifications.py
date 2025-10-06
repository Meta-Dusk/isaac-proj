import flet as ft


def simple_notification(content: ft.StrOrControl, page: ft.Page):
    snackbar = ft.SnackBar(
        content=content, open=True,
        duration=1000, behavior=ft.SnackBarBehavior.FLOATING,
        on_dismiss=lambda e: page.overlay.remove(e.control)
    )
    page.overlay.append(snackbar)