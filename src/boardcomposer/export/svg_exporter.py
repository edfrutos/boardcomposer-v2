from boardcomposer.domain import AssemblySolution


def solution_to_svg(solution: AssemblySolution) -> str:
    width = solution.total_length_mm
    height = solution.total_width_mm

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
    ]

    for placement in solution.placements:
        parts.append(
            f'<rect x="{placement.x_mm}" y="{placement.y_mm}" '
            f'width="{placement.length_mm}" height="{placement.width_mm}" '
            f'fill="none" stroke="black" />'
        )
        parts.append(
            f'<text x="{placement.x_mm + 5}" y="{placement.y_mm + 20}" font-size="16">'
            f"{placement.board_id}</text>"
        )

    parts.append("</svg>")
    return "\n".join(parts)
