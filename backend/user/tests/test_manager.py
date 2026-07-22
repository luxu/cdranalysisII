import pytest
from django.contrib.auth import get_user_model
from django.test.utils import override_settings

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestCreateSuperuserValidation:
    def test_create_superuser_with_is_staff_false_raises_error(self):
        with pytest.raises(ValueError, match='is_staff=True'):
            User.objects.create_superuser(
                email='admin@example.com', password='admin', is_staff=False,
            )

    def test_create_superuser_with_is_superuser_false_raises_error(self):
        with pytest.raises(ValueError, match='is_superuser=True'):
            User.objects.create_superuser(
                email='admin@example.com', password='admin', is_superuser=False,
            )


class _BackendWithoutWithPerm:
    def authenticate(self, request, **kwargs):
        return None
    def get_user(self, user_id):
        return None


class TestWithPerm:
    def test_with_perm_non_string_backend_raises_type_error(self):
        with pytest.raises(TypeError):
            User.objects.with_perm('some_perm', backend=42)

    def test_with_perm_string_backend_returns_queryset(self):
        qs = User.objects.with_perm(
            'auth.change_user', backend='django.contrib.auth.backends.ModelBackend',
        )
        assert list(qs) == []

    def test_with_perm_backend_none_multiple_backends(self):
        with override_settings(AUTHENTICATION_BACKENDS=[
            'django.contrib.auth.backends.ModelBackend',
            'django.contrib.auth.backends.AllowAllUsersModelBackend',
        ]):
            with pytest.raises(ValueError, match='multiple authentication backends'):
                User.objects.with_perm('auth.change_user')

    def test_with_perm_backend_without_with_perm(self):
        with override_settings(AUTHENTICATION_BACKENDS=[
            'user.tests.test_manager._BackendWithoutWithPerm',
        ]):
            qs = User.objects.with_perm('auth.change_user')
            assert list(qs) == []
