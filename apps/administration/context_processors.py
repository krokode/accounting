from apps.administration.models import CompanyProfile


def company_profile_processor(request):
    """Makes the active company organization profile available across all templates."""
    try:
        profile = CompanyProfile.get_solo()
    except Exception:
        profile = None
    return {
        'active_company_profile': profile
    }
