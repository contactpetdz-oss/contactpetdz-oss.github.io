# PetDZ 🐾

**PetDZ** est un agrégateur de promotions et un service de petites annonces pour animaux de compagnie (chiens et chats) en Algérie. Le site est conçu pour aider les propriétaires à trouver les meilleures offres sur les croquettes, accessoires, jouets, etc., et à publier des annonces de vente, adoption ou pension.

👉 **Site en ligne** : [contactpetdz-oss.github.io](https://contactpetdz-oss.github.io)

---

## ✨ Fonctionnalités

- **Promos & ventes flash** : Affichage quotidien des meilleures offres issues de Temu, AliExpress et d'autres sources.
- **Achat par procuration** : Service permettant de commander pour vous sur des sites étrangers si votre carte CIB/EDAHABIA ne fonctionne pas (commission 12% + 500 DA).
- **Abonnement Premium** : Accès à des deals exclusifs, alertes WhatsApp, commission réduite, etc. (700 DA/mois).
- **Petites annonces** : Publication d'annonces pour vendre, adopter ou proposer des services (300 DA par annonce).
- **Conseil et citation du jour** : Chaque jour, un conseil d'élevage et une citation sur les animaux s'affichent automatiquement.

---

## 🛠️ Technologies utilisées

- **Frontend** : HTML / CSS / JavaScript (fichier unique `index.html`)
- **Hébergement** : GitHub Pages (gratuit)
- **Automatisation** : GitHub Actions (mise à jour quotidienne des produits)
- **Paiements** : Chargily Pay (en cours d'activation) / contact direct par WhatsApp en attendant

---

## 📦 Structure du dépôt

---

## 🤖 Fonctionnement de l'automatisation

Chaque jour à 6h UTC, le workflow GitHub Actions exécute `update_products.py` qui :

1. Récupère des produits depuis l'API de recherche de Temu (avec plusieurs mots-clés).
2. Ajoute des produits statiques (base).
3. Génère le fichier `products.json` qui alimente la page d'accueil.
4. Commit et push automatiquement la mise à jour.

---

## 🔧 Installation en local (pour contribuer)

1. Clone le dépôt :
   ```bash
   git clone https://github.com/contactpetdz-oss/contactpetdz-oss.github.io.git
