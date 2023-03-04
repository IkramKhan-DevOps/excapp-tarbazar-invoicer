from src.accounts.models import Company


def get_company_profile_bll():
    return Company.objects.first() if Company.objects.all() else Company.objects.create(name='no-name', tagline='__ no tagline __', description='__no description available__')
