import flet as ft


def default_row(controls: list[ft.Control]) -> ft.Row:
    return ft.Row(
        controls=controls,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        run_alignment=ft.MainAxisAlignment.CENTER,
        spacing=8, run_spacing=8
    )

def default_column(controls: list[ft.Control]) -> ft.Column:
    return ft.Column(
        controls=controls,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        run_alignment=ft.MainAxisAlignment.CENTER,
        expand=True, spacing=8, run_spacing=8
    )
    
def default_container(
    content: ft.Control,
    bgcolor: ft.ColorValue = ft.Colors.SURFACE_CONTAINER_LOWEST
) -> ft.Control:
    return ft.Container(
        content=content, padding=16, border_radius=8,
        bgcolor=bgcolor, alignment=ft.Alignment.CENTER
    )

def default_drag_area(content: ft.Control) -> ft.WindowDragArea:
    return ft.WindowDragArea(
        content=content, expand=True, maximizable=False
    )