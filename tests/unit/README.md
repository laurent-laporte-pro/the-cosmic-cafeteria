# Tests Unitaires pour The Cosmic Cafeteria

Ce répertoire contient les tests unitaires pour l'API de The Cosmic Cafeteria. Les tests suivent les meilleures pratiques pour tester une application Flask, en se concentrant sur le test des composants individuels en isolation.

## Organisation des Tests

Les tests unitaires sont organisés par composant:

- `test_app_factory.py` : Tests pour la fabrique d'application Flask
- `test_cli_commands.py` : Tests pour les commandes CLI
- `test_meal_routes.py` : Tests pour les points d'accès API liés aux repas
- `test_models.py` : Tests pour les modèles de base de données
- `test_order_routes.py` : Tests pour les points d'accès API liés aux commandes
- `test_routes.py` : Tests pour les routes API
- `test_schemas.py` : Tests pour les schémas API
- `test_utils.py` : Tests pour les fonctions utilitaires
- `test_worker_tasks.py` : Tests pour les tâches asynchrones

## Exécution des Tests

Vous pouvez exécuter les tests unitaires à l'aide du script fourni:

```bash
./run_unit_tests.sh
```

Ou les exécuter directement avec pytest:

```bash
python -m pytest tests/unit/ -v --cov=src
```

## Rapport de Couverture

Après l'exécution des tests, un rapport de couverture sera généré dans le répertoire `htmlcov`. Vous pouvez ouvrir `htmlcov/index.html` dans un navigateur web pour consulter le rapport.

## Rédaction de Nouveaux Tests

Lors de l'ajout de nouvelles fonctionnalités à l'application, assurez-vous d'ajouter les tests unitaires correspondants. Suivez ces directives:

1. **Tester en isolation** : Utilisez des mocks pour les dépendances externes
2. **Nommer les tests clairement** : Utilisez des noms descriptifs qui expliquent ce qui est testé
3. **Suivre le modèle AAA** : Arrange (Préparer), Act (Agir), Assert (Vérifier)
4. **Tester les cas limites** : Incluez des tests pour les conditions d'erreur et les cas limites
5. **Garder les tests indépendants** : Chaque test doit s'exécuter indépendamment des autres

## Fixtures de Test

Les fixtures de test communes sont définies dans `conftest.py`. Utilisez ces fixtures dans vos tests pour éviter la duplication de code.

## Intégration Continue

Les tests unitaires sont exécutés automatiquement sur GitHub Actions lorsque le code est poussé vers le dépôt. Consultez le fichier `.github/workflows/unit-tests.yml` pour plus de détails sur la configuration CI.
