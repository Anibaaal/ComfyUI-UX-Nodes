def validate_hex_color(hex_color):
    """Validate hex color format."""
    if not hex_color.startswith('#'):
        hex_color = f'#{hex_color}'
    
    if len(hex_color) != 7:
        raise ValueError("Invalid hex color format. Expected format: #RRGGBB")
    
    try:
        int(hex_color[1:], 16)
        return hex_color
    except ValueError:
        raise ValueError("Invalid hex color format. Expected format: #RRGGBB")

def lerp(start: float, end: float, t: float) -> float:
    """Linear interpolation between start and end values.
    
    Args:
        start: Starting value
        end: Ending value
        t: Interpolation factor (0.0 to 1.0)
    
    Returns:
        Interpolated value
    """
    return start + (end - start) * t