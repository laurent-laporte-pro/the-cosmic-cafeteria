---
title: Introduction
description: Introduction et présentation des objectifs
---

# ✨ Qu'est-ce que c'est ?

**La Cafétéria Cosmique** est une application web fantaisiste où des super-héros voyageant dans l'espace peuvent
commander leurs repas préférés à travers la galaxie.

Construite pour tester et mettre en valeur des compétences techniques autour de Python, Flask, les files d'attente
asynchrones, les tests et la modélisation de bases de données.

# 🧪 Ingrédients techniques

| Ingrédient          | Objectif                                 |
|---------------------|------------------------------------------|
| 🐍 Python 3.12      | Langage principal                        |
| 🔥 Flask            | Framework web                            |
| 🗃️ PostgreSQL      | Base de données relationnelle            |
| 🧙 SQLAlchemy       | ORM pour la magie des bases de données   |
| 🐿️ Redis           | Message broker / file d'attente          |
| 🔁 RQ (Redis Queue) | Traitement des tâches en arrière-plan    |
| 🧪 Pytest           | Tests unitaires & d'intégration          |
| 🐳 Docker           | Orchestration d'environnement & services |
| 📜 Docstrings       | Documentation API                        |
| 📋 Logging          | Suivi des événements & débogage          |

# 🦸‍♂️ Fonctionnalités de l'application

- Lister, créer, mettre à jour et supprimer des **héros** avec leurs informations d'allergies
- Gérer des **repas galactiques** avec des ingrédients exotiques
- Créer des **commandes** — vérifiées automatiquement pour les allergènes
- Les commandes sont traitées de manière asynchrone via **Redis Queue**
- Chaque action est **journalisée** pour la transparence et la facilité de débogage
- Backend entièrement **testé** avec pytest
- Configuration **Docker** pour le développement local

# 🧑🏻‍🏫 Instructions pour ce test technique

L'objectif de ce test technique est d'évaluer vos compétences en développement d'application web (avec Flask),
en gestion de base de données (PostgreSQL), en gestion de files d'attente (Redis) et en tests unitaires (Pytest)
et en Infrastructure as Code (Docker).

Les éléments **hors périmètre** de ce test technique incluent l'UI/UX, l'authentification,
l'utilisation de Celery et l'optimisation des performances.

Votre mission, si vous l'acceptez, est de créer deux petites applications :

- Une webapp pour gérer les héros et les repas
- Un worker pour traiter les commandes en arrière-plan

Vous devrez implémenter cette application en utilisant les technologies mentionnées ci-dessus
et mettre en place l'infrastructure nécessaire pour la faire fonctionner avec Docker.

Consultez les [Spécifications Techniques](02-specs.md) pour les détails sur les fonctionnalités à implémenter.
