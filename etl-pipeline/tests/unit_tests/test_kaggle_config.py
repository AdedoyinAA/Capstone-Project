import os
import pytest
from config.kaggle_config import load_kaggle_config, KaggleConfigurationError


def test_load_kaggle_config(mocker):
    # Mock environment variables
    mocker.patch.dict(os.environ, {
        'KAGGLE_USERNAME': 'test_username',
        'KAGGLE_KEY': 'test_key'
    })

    config = load_kaggle_config()

    assert config['kaggle']['username'] == 'test_username'
    assert config['kaggle']['key'] == 'test_key'


def test_load_kaggle_config_missing_env_var_key_defaults(mocker):
    # Mock environment variables with one missing
    mocker.patch.dict(os.environ, {
        'KAGGLE_USERNAME': 'test_username',
        # 'KAGGLE_KEY': 'test_key' # Missing
    })

    config = load_kaggle_config()

    assert config['kaggle']['username'] == 'test_username'
    assert config['kaggle']['key'] == ""  # Default value


# Mapping from environment variables names to configuration keys
env_var_to_config_key = {
    'KAGGLE_USERNAME': 'username',
    'KAGGLE_KEY': 'key'
}


@pytest.mark.parametrize("env_var", [
    'KAGGLE_USERNAME',
    'KAGGLE_KEY'
])
def test_load_kaggle_config_missing_env_var_errors(mocker, env_var):
    # Mock environment variables with one set to 'error'
    mock_env = {
        'KAGGLE_USERNAME': 'test_username',
        'KAGGLE_KEY': 'test_key'
    }
    mock_env[env_var] = 'error'  # Set the parametrized env_var to 'error'
    mocker.patch.dict(os.environ, mock_env)

    config_key = env_var_to_config_key[env_var]

    with pytest.raises(KaggleConfigurationError, match=(
        f"Configuration error: kaggle {config_key} is set to 'error'"
    )):
        load_kaggle_config()
