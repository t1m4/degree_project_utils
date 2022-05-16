from dataclasses import dataclass


@dataclass
class Profile:
    company_id: int


@dataclass
class User:
    email: str
    company_id: int
    profile: Profile
    is_authenticated: bool
    has_financial_access: bool
    id: int
    first_name: str
    last_name: str
    is_test: bool
    is_admin: bool = False

    @classmethod
    def init_x_auth_data(cls, user_data):
        """
        Initialize User object from decoded JWT token of X_INTERNAL_AUTHORIZATION header
        """
        return cls(
            email=user_data['email'],
            company_id=user_data['company_id'],
            profile=Profile(company_id=user_data['company_id']),
            is_authenticated=True,
            has_financial_access=user_data['has_financial_access'],
            id=user_data['id'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            is_admin=user_data['is_admin_user'],
            is_test=user_data['is_test'],
        )
