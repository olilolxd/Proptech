# 🏡 Proptech Dashboard - Montréal

Ce projet est un outil d'analyse immobilière hybride combinant l'extraction de données du marché (Realtor/Centris) avec un modèle financier avancé incluant les avantages du **CELIAPP**.

## 🚀 Comment l'utiliser

### 1. Installation des dépendances

Il est recommandé d'utiliser un environnement virtuel.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
```

*(Optionnel) `playwright install` est nécessaire uniquement si vous n'avez pas déjà les navigateurs Playwright d'installés pour le module d'extraction de données.*

### 2. Extraction des données (Optionnel)

Le tableau de bord est fourni avec un générateur de données de *fallback* pour fonctionner immédiatement. Si vous voulez récupérer les VRAIS prix actuels depuis le site web Realtor, roulez l'extracteur :

```bash
python data_extractor.py
```

*Note: Realtor peut parfois bloquer les connexions automatisées. Si tel est le cas, le script va automatiquement générer le *fallback* `listings_montreal.csv` pour que le dashboard fonctionne.*

### 3. Lancer le Tableau de Bord

```bash
streamlit run app.py
```

Le tableau de bord s'ouvrira dans votre navigateur web à l'adresse `http://localhost:8501`.

## 🗂 Structure du projet

- `app.py` : Application principale Streamlit (interface utilisateur).
- `data_extractor.py` : Script d'automatisation Playwright pour aller chercher les annonces.
- `financial_model.py` : Cœur de la logique mathématique (Calcul hypothécaire, CELIAPP, Flux de trésorerie).
- `test_financials.py` : Tests unitaires pour valider les modèles financiers via `pytest`.

## 📊 Modèle CELIAPP

Le CELIAPP permet de cotiser 8 000 $ par an jusqu'à 40 000 $. La déduction fiscale (estimée via le taux marginal d'imposition) est calculée et **réinvestie directement dans la mise de fonds** pour bonifier la rentabilité (Cash-on-Cash Return).
