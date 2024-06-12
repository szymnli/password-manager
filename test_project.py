import pytest
from unittest.mock import patch, MagicMock
from project import Vault, password_generator, authenticate, empty_vault

master_key = "master_test"
vault = Vault(master_key)


@pytest.fixture
def mock_vault():
    vault = MagicMock()
    vault.authenticate = MagicMock(return_value=True)
    return vault


def test_authenticate(mock_vault):
    _master_key = "_master_key"
    encrypted_master_key = "encrypted_master_key"

    with patch("click.prompt", return_value=_master_key), patch(
        "cryptmoji.encrypt", return_value=encrypted_master_key
    ):
        assert authenticate(mock_vault) == True
        mock_vault.authenticate.assert_called_once_with(encrypted_master_key)


def test_password_generator():
    password = password_generator(vault, 30)
    assert password.isalpha() == False
    assert len(password) == 30


def test_vault():
    assert vault.master_key == master_key
    assert vault.passwords == {}


def test_add_password():
    vault.add_password("gmail", "username123", "password123")
    assert vault.passwords == {
        "gmail": {"Username": "username123", "Password": "password123"}
    }
    assert vault != {}


def test_get_password():
    vault.add_password("gmail", "username123", "password123")
    assert vault.get_password("gmail") == {
        "Username": "username123",
        "Password": "password123",
    }


def test_delete_password():
    vault.add_password("gmail", "username123", "password123")
    vault.delete_password("gmail")
    assert vault.passwords == {}


def test_empty_vault():
    vault.add_password("gmail", "username123", "password123")
    assert vault.passwords == {
        "gmail": {"Username": "username123", "Password": "password123"}
    }
    _vault = empty_vault(vault)
    assert str(_vault) == str(Vault(master_key, {}))
