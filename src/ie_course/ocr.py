
def group_into_lines(results, y_threshold=10):
    """
    Groups OCR results into lines based on vertical proximity.
    """
    # compute center y for each box
    items = []
    for bbox, text, conf in results:
        ys = [pt[1] for pt in bbox]
        xs = [pt[0] for pt in bbox]
        cy = sum(ys) / 4
        cx = min(xs)
        items.append((cy, cx, text, conf))

    # sort top → bottom
    items.sort(key=lambda x: x[0])

    lines = []
    current_line = []
    current_y = None

    for cy, cx, text, conf in items:
        if current_y is None or abs(cy - current_y) <= y_threshold:
            current_line.append((cx, text))
            current_y = cy if current_y is None else current_y
        else:
            # finalize line
            lines.append(current_line)
            current_line = [(cx, text)]
            current_y = cy

    if current_line:
        lines.append(current_line)

    return lines

def lines_to_markdown(lines):
    md_lines = []

    for line in lines:
        # sort left → right
        line = sorted(line, key=lambda x: x[0])

        texts = [t for _, t in line]

        # join with spaces but preserve structure
        md_lines.append(" ".join(texts))

    return "\n".join(md_lines)