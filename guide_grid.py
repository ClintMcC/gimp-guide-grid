from gimpfu import *

def guide_grid(image, drawable, hspace, vspace, percent, hgutter, vgutter, hmargin, vmargin, delete_guides):
    pdb.gimp_image_undo_group_start(image)
    
    # Delete all existing guides if requested.
    if delete_guides:
        guides = pdb.gimp_image_find_next_guide(image, 0)
        while guides != 0:
            pdb.gimp_image_remove_guide(image, guides)
            guides = pdb.gimp_image_find_next_guide(image, 0)

    imageHeight = pdb.gimp_image_height(image)
    imageWidth = pdb.gimp_image_width(image)

    if percent == 1:
        # Recalculate pixel spacing by percentage.
        hspace = int(hspace * (imageHeight * 0.01))
        vspace = int(vspace * (imageWidth * 0.01))

    # Input validity check.
    if hspace <= 0 or vspace <= 0 or hmargin < 0 or vmargin < 0:
        return

    # Calculate usable width and height after margins.
    usableHeight = imageHeight - 2 * vmargin
    usableWidth = imageWidth - 2 * hmargin

    if usableHeight <= 0 or usableWidth <= 0:
        return  # Exit if margins make the grid impossible.

    # Add guides at the margins.
    pdb.gimp_image_add_hguide(image, vmargin)  # Top margin
    pdb.gimp_image_add_hguide(image, imageHeight - vmargin)  # Bottom margin
    pdb.gimp_image_add_vguide(image, hmargin)  # Left margin
    pdb.gimp_image_add_vguide(image, imageWidth - hmargin)  # Right margin

    # Calculate the number of grid cells.
    hCells = int(usableHeight / (hspace + hgutter))
    vCells = int(usableWidth / (vspace + vgutter))

    # Add the horizontal guides (including gutter lines).
    for i in range(1, hCells + 1):
        # Grid line (bottom border of each cell)
        y_grid = vmargin + i * (hspace + hgutter)
        if y_grid < imageHeight - vmargin:
            pdb.gimp_image_add_hguide(image, y_grid)

        # Gutter start (top border of gutter)
        if hgutter > 0:
            y_gutter = y_grid - hgutter
            if vmargin < y_gutter < imageHeight - vmargin:
                pdb.gimp_image_add_hguide(image, y_gutter)

    # Add the vertical guides (including gutter lines).
    for i in range(1, vCells + 1):
        # Grid line (right border of each cell)
        x_grid = hmargin + i * (vspace + vgutter)
        if x_grid < imageWidth - hmargin:
            pdb.gimp_image_add_vguide(image, x_grid)

        # Gutter start (left border of gutter)
        if vgutter > 0:
            x_gutter = x_grid - vgutter
            if hmargin < x_gutter < imageWidth - hmargin:
                pdb.gimp_image_add_vguide(image, x_gutter)

    pdb.gimp_image_undo_group_end(image)


register(
    "python_fu_guide_grid",
    "Guide Grid with Gutter, Margin, and Option to Clear Guides",
    "Creates a grid of guides with specified spacing, gutters, and margins, and optionally clears existing guides.",
    "Theodoros Balasis", "", "2025",
    "Guide Grid with Gutter, Margin, and Clear Option",
    "*",
    [
        (PF_IMAGE, "image", "Input Image", None),
        (PF_DRAWABLE, "drawable", "Input Layer", None),
        (PF_FLOAT, "hspace", "Horizontal Spacing", 50.0),
        (PF_FLOAT, "vspace", "Vertical Spacing", 50.0),
        (PF_BOOL, "percent", "By percent?", 0),
        (PF_INT, "hgutter", "Horizontal Gutter (px)", 0),
        (PF_INT, "vgutter", "Vertical Gutter (px)", 0),
        (PF_INT, "hmargin", "Horizontal Margin (px)", 0),
        (PF_INT, "vmargin", "Vertical Margin (px)", 0),
        (PF_BOOL, "delete_guides", "Delete all existing guides?", 0),
    ],
    [],
    guide_grid,
    menu="<Image>/Image/Guides"
)

main()
