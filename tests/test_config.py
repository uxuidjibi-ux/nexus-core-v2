from nexus.config import Settings


def test_defaults_are_safe():
    settings = Settings(_env_file=None)
    assert settings.nexus_dry_run is True
    assert settings.sandbox_timeout_seconds <= 120


def test_urls_are_normalized():
    settings = Settings(_env_file=None, wp_url="https://example.test///")
    assert settings.wp_url == "https://example.test"
