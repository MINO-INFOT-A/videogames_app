TRANSLATIONS = {
    'es': {
        'nav_home': 'Inicio',
        'nav_forum': 'Foros',
        'nav_collection': 'Mi Colección',
        'nav_login': 'Entrar',
        'nav_logout': 'Salir',
        'news_title': 'Últimas Noticias',
        'collection_title': 'Tu Bóveda de Juegos',
    },
    'en': {
        'nav_home': 'Home',
        'nav_forum': 'Forums',
        'nav_collection': 'My Collection',
        'nav_login': 'Login',
        'nav_logout': 'Logout',
        'news_title': 'Latest News',
        'collection_title': 'Your Game Vault',
    }
}

def get_translation(lang, key):
    return TRANSLATIONS.get(lang, TRANSLATIONS['es']).get(key, key)
