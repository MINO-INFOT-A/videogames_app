from app import create_app, db
from app.models import User, News, ForumThread, ForumPost, CollectionItem
from werkzeug.security import generate_password_hash

app = create_app()

def seed():
    with app.app_context():
        db.create_all() # Ensure tables exist

        # Crear usuario demo
        demo_user = User.query.filter_by(username='demo').first()
        if not demo_user:
            demo_user = User(username='demo', password_hash=generate_password_hash('demo', method='scrypt'))
            db.session.add(demo_user)
            db.session.commit()
            print("Usuario 'demo' creado.")

        # Inyectar Noticias
        if News.query.count() == 0:
            news_items = [
                News(title="Nintendo anuncia la sucesora de la Switch", content="Los últimos rumores indican que Nintendo presentará su nueva consola a finales de este año. La expectación es máxima entre los fans de lo retro y lo moderno."),
                News(title="El resurgir de los juegos Indie estilo PS1", content="La estética low-poly de la primera PlayStation vuelve a estar de moda. Descubre los títulos que están triunfando con este apartado visual nostálgico."),
                News(title="Speedrun de Super Mario 64 rompe récord", content="Un jugador ha logrado completar el juego en un tiempo nunca antes visto, utilizando una nueva técnica descubierta tras años de investigación en la comunidad."),
                News(title="Análisis cruzado: Modern Warfare vs GoldenEye 007", content="Un repaso a cómo ha evolucionado el género de los shooters desde la época de Nintendo 64 hasta las consolas de última generación."),
                News(title="El modding en PC mantiene viva la esencia clásica", content="Mods recientes demuestran cómo la comunidad es capaz de revitalizar juegos con más de 20 años a sus espaldas, añadiendo texturas HD y nuevas campañas.")
            ]
            db.session.add_all(news_items)
            print("Noticias añadidas.")

        # Inyectar Foros
        if ForumThread.query.count() == 0:
            threads = [
                ForumThread(title="¿Cuál fue vuestra primera consola?", author_id=demo_user.id),
                ForumThread(title="Recomendaciones de RPGs ocultos de SNES", author_id=demo_user.id),
                ForumThread(title="¿Opiniones sobre la realidad virtual en 2026?", author_id=demo_user.id)
            ]
            db.session.add_all(threads)
            db.session.commit()
            
            # Posts
            post1 = ForumPost(content="La mía fue la Master System II con Alex Kidd en memoria. ¡Qué recuerdos!", thread_id=threads[0].id, author_id=demo_user.id)
            post2 = ForumPost(content="Si no habéis jugado a Terranigma, os lo estáis perdiendo.", thread_id=threads[1].id, author_id=demo_user.id)
            post3 = ForumPost(content="Creo que aún le falta ser más accesible, pero está mejorando.", thread_id=threads[2].id, author_id=demo_user.id)
            db.session.add_all([post1, post2, post3])
            print("Hilos y posts del foro añadidos.")

        # Inyectar Colección (CollectionItem)
        if CollectionItem.query.filter_by(user_id=demo_user.id).count() == 0:
            games = [
                CollectionItem(user_id=demo_user.id, game_title="The Legend of Zelda: Ocarina of Time", platform="Nintendo 64", status="Completed"),
                CollectionItem(user_id=demo_user.id, game_title="Final Fantasy VII", platform="PlayStation", status="Completed"),
                CollectionItem(user_id=demo_user.id, game_title="Hollow Knight", platform="PC", status="Playing"),
                CollectionItem(user_id=demo_user.id, game_title="Super Metroid", platform="SNES", status="Completed"),
                CollectionItem(user_id=demo_user.id, game_title="Elden Ring", platform="PS5", status="Unplayed")
            ]
            db.session.add_all(games)
            print("Juegos añadidos a la colección del usuario demo.")

        db.session.commit()
        print("¡Base de datos populada con éxito!")

if __name__ == '__main__':
    seed()
