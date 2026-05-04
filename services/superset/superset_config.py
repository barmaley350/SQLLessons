SECRET_KEY = "2d9fd294aa390df0360036992ded4db6c30a962a3b05375c05a4e438ea40e433"
PREVENT_UNSAFE_DB_CONNECTIONS = False
FEATURE_FLAGS = {"ENABLE_TEMPLATE_PROCESSING": True, "DRILL_TO_DETAIL": True}


LANGUAGES = {
    "ru": {"flag": "ru", "name": "Русский"},
    "en": {"flag": "us", "name": "English"},
}

BABEL_DEFAULT_LOCALE = "en"
