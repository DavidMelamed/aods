try:
    from .plots import scatter_roi_vs_cost  # type: ignore
except Exception:  # matplotlib may be missing
    def scatter_roi_vs_cost(*args, **kwargs):  # type: ignore
        raise ImportError("matplotlib not installed")

__all__ = ['scatter_roi_vs_cost']
