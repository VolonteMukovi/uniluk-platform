# Plateforme UNILUK

Backend Django + Django REST Framework, avec un espace de gestion indépendant à `/dashboard/`, et frontend Alpine existant relié à l’API.

## Installation

1. Créez la base MySQL encodée en `utf8mb4` : `CREATE DATABASE uniluk CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`.
2. Créez et activez un environnement virtuel, puis exécutez `pip install -r requirements.txt`.
3. Exportez les variables de `.env.example` (ou configurez-les dans votre environnement).
4. Lancez `python manage.py makemigrations core`, `python manage.py migrate`, puis chargez le contenu initial avec `mysql -u root uniluk < database/uniluk_seed.sql`. Enfin, créez l’administrateur avec `python manage.py createsuperuser`.
5. Démarrez avec `python manage.py runserver` et ouvrez `http://127.0.0.1:8000/`.

## Gestion

Tous les éléments éditoriaux sont gérés dans le dashboard : identité/coordonnées, slides hero, statistiques, facultés et programmes, actualités, communiqués/PDF, institutions, groupes, bâtiments, services, galerie, témoignages, pages statiques et inscriptions. Chaque média accepte un téléversement local ou une URL externe.

L’API REST est sous `/api/`. Les lectures publiées sont accessibles au site; les opérations d’écriture REST nécessitent une session d’administrateur. La galerie utilise la pagination de l’API côté client.

Le script [uniluk_seed.sql](F:\front UNILUK\database\uniluk_seed.sql) contient toutes les collections éditoriales actuelles du template. Sa source reproductible est [generate_seed_sql.js](F:\front UNILUK\scripts\generate_seed_sql.js) ; relancez-la uniquement si vous modifiez les données statiques avant l’import initial.
"# uniluk-platform" 
