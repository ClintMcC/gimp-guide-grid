from gimpfu import *

def guide_grid(image, drawable, hspace, vspace, percent, hgutter, vgutter, hmargin, vmargin):
    pdb.gimp_image_undo_group_start(image)
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

    # Calculate the number of guides.
    hGuides = int(usableHeight / (hspace + hgutter))
    vGuides = int(usableWidth / (vspace + vgutter))

    # Add horizontal guides.
    for i in range(hGuides + 1):
        y = vmargin + i * (hspace + hgutter)
        if y < imageHeight - vmargin:
            pdb.gimp_image_add_hguide(image, y)

    # Add vertical guides.
    for i in range(vGuides + 1):
        x = hmargin + i * (vspace + vgutter)
        if x < imageWidth - hmargin:
            pdb.gimp_image_add_vguide(image, x)

    pdb.gimp_image_undo_group_end(image)


register(
    "python_fu_guide_grid",
    "Guide Grid with Gutter and Margin",
    "Creates a grid of guides with specified spacing, gutters, and margins.",
    "Theodoros Balasis", "", "2025",
    "Guide Grid with Gutter and Margin",
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
    ],
    [],
    guide_grid,
    menu="<Image>/Image/Guides"
)

main()
