from ipware import get_client_ip

def detect_indian_region(request):
    """
    Very lightweight heuristic-based region mapping.
    Can be improved later with MaxMind / API.
    """
    ip, _ = get_client_ip(request)

    # Development / localhost
    if not ip or ip.startswith("127.") or ip == "localhost":
        return {
            "zone": "HOT-HUMID",
            "label": "Tropical / Hot-Humid India",
            "notes": "Typical Indian tropical conditions with heat stress risk"
        }

    # ⚠️ Placeholder: real IP-to-region mapping can be added later
    return {
        "zone": "SUB-TROPICAL",
        "label": "Sub-tropical India",
        "notes": "Moderate summers, cool winters"
    }
