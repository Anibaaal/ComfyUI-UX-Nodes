class LerpNode:
    """Node that performs linear interpolation between two float values."""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "start": ("FLOAT", {
                    "default": 0.0, 
                    "min": -10000.0,
                    "max": 10000.0,
                    "step": 0.01
                }),
                "end": ("FLOAT", {
                    "default": 1.0,
                    "min": -10000.0,
                    "max": 10000.0,
                    "step": 0.01
                }),
                "t": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                })
            }
        }
    
    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "interpolate"
    CATEGORY = "math"
    
    def interpolate(self, start: float, end: float, t: float) -> tuple[float]:
        """Perform linear interpolation between start and end values.
        
        Args:
            start: Starting value
            end: Ending value
            t: Interpolation factor (0.0 to 1.0)
            
        Returns:
            Tuple containing the interpolated value
        """
        from ..utils.color_utils import lerp
        result = lerp(start, end, t)
        return (result,)