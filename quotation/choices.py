SERVICE_CHOICES = (
    (1, "Business To Business"),
    (2, "Hand To Hand"),
    (3, "Direct Mail"),
    (4, "Residential Homes"),
    (5, "Shared Distribution"),
    (6, "Consultation Distribution"),
)

BOX_TO_COLLECT = (
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4 or more"),
    (5, "N/A"),
)

TYPE_OF_MEDIA = (
    (1, "Flyer"),
    (2, "Leaflet"),
    (3, "Folded Leaflet"),
    (4, "Other"),
)

REQUIRE_COLLECTION = (
    (1, "Yes"),
    (2, "No"),
)

PAGES = (
    (1, "Single Sided"),
    (2, "Double Sided"),
    (3, "2 Pages"),
    (4, "4 Pages"),
    (5, "6 Pages"),
    (6, "8 Pages"),
    (7, "10 Pages"),
    (8, "12 Pages"),
)

PAGE_ORIENTATION = (
    (1, "Portrait"),
    (2, "Landscape"),
)

COLORS = (
    (1, "1/0-coloured Black"),
    (2, "2/0-coloured Black + Pantone"),
    (3, "2/0-coloured Black + Gold"),
    (4, "4/0-coloured CMYK"),
)

PROCESSING = (
    (1, "Trimming"),
    (2, "Trimming Corner Rounded"),
)

STATUS_CHOICES = (
    (1, "New"),
    (2, "Reviewed"),
    (3, "Accepted"),
)
