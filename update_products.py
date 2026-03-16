import requests
import json
import os
import time
import random
from datetime import datetime

# ===== CONFIGURATION =====
# Utilise les variables d'environnement (secrets GitHub) pour les tokens
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')  # À définir dans les secrets
REPO = "contactpetdz-oss/contactpetdz-oss.github.io"
BRANCH = "main"

# Identifiants d'affiliation (optionnels)
TEMU_AFF_ID = os.environ.get('TEMU_AFFILIATE_ID', '')

# Liens AliExpress statiques
ALI_LINKS = [
    'https://s.click.aliexpress.com/e/_c3Qyu8yn',
    'https://s.click.aliexpress.com/e/_c4UF0X5V',
    'https://s.click.aliexpress.com/e/_c4DRN5YL',
]

# Produits de base (statiques)
BASE_PRODUCTS = [
    {'id':1,'type':'flash','animal':'chien','cat':'alimentation','name':'Royal Canin Medium Adult 15kg','src':'Temu','plat':'temu','op':6800,'np':4200,'end_hours':6,'link':'https://temu.to/k/e6c3s5aetpv','desc':'Croquettes premium chiens.'},
    {'id':2,'type':'flash','animal':'chat','cat':'alimentation','name':'Purina Pro Plan Saumon 10kg','src':'Temu','plat':'temu','op':5200,'np':2900,'end_hours':8,'link':'https://temu.to/k/e6sv54vok7h','desc':'Aliment complet chats adultes.'},
    {'id':3,'type':'flash','animal':'chien','cat':'sante','name':'Antiparasitaire Spot-On x6','src':'Temu','plat':'temu','op':2800,'np':980,'end_hours':5,'link':'https://temu.to/k/ehntxv1jh73','desc':'Protection puces et tiques.'},
    {'id':4,'type':'flash','animal':'chat','cat':'accessoire','name':'Griffoir Arbre a Chat 4 Niveaux','src':'Temu','plat':'temu','op':3500,'np':1400,'end_hours':12,'link':'https://temu.to/k/efi1scl4z9v','desc':'Griffoirs sisal naturel.'},
    {'id':5,'type':'flash','animal':'chien','cat':'accessoire','name':'Collier GPS Tracker Chien','src':'Temu','plat':'temu','op':4200,'np':2100,'end_hours':7,'link':'https://temu.to/k/esl7kn0x2v7','desc':'GPS temps reel.'},
    {'id':6,'type':'flash','animal':'chien','cat':'alimentation','name':'Alimentation Premium Chien','src':'AliExpress','plat':'aliexpress','op':4800,'np':2200,'end_hours':10,'link':ALI_LINKS[0],'desc':'Nourriture complete chien adulte.'},
    {'id':7,'type':'flash','animal':'chat','cat':'alimentation','name':'Nourriture Premium Chat 5kg','src':'AliExpress','plat':'aliexpress','op':3200,'np':1450,'end_hours':14,'link':ALI_LINKS[1],'desc':'Aliment complet chat adulte.'},
    {'id':8,'type':'sale','animal':'chien','cat':'accessoire','name':'Kit Accessoires Animaux','src':'AliExpress','plat':'aliexpress','op':2600,'np':980,'end_hours':None,'link':ALI_LINKS[2],'desc':'Accessoires complets.'},
    {'id':9,'type':'sale','animal':'chat','cat':'hygiene','name':'Shampoing Demelant Poils Longs','src':'Temu','plat':'temu','op':980,'np':390,'end_hours':None,'link':'https://temu.to/k/efi1scl4z9v','desc':'Formule douce.'},
    {'id':10,'type':'sale','animal':'chien','cat':'sante','name':'Kit Hygiene Dentaire Veterinaire','src':'Temu','plat':'temu','op':1200,'np':620,'end_hours':None,'link':'https://temu.to/k/esl7kn0x2v7','desc':'Previent le tartre.'},
    {'id':11,'type':'sale','animal':'chat','cat':'accessoire','name':'Maison Transport Rigide Taille M','src':'Temu','plat':'temu','op':3800,'np':1650,'end_hours':None,'link':'https://temu.to/k/efi1scl4z9v','desc':'Verrou securise.'},
    {'id':12,'type':'sale','animal':'chien','cat':'hygiene','name':'Table Toilettage Pliable Pro','src':'Temu','plat':'temu','op':8500,'np':4200,'end_hours':None,'link':'https://temu.to/k/e6c3s5aetpv','desc':'Table pliable pro.'},
]

# ===== FONCTIONS =====
def fetch_temu_products():
    """Récupère les produits en direct depuis Temu via l'API de recherche."""
    live = []
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36'}
    pid = 200  # ID de départ pour les produits dynamiques
    # Mots-clés à rechercher
    keywords = [('dog food', 'chien'), ('cat food', 'chat'), ('dog toy', 'chien'), ('cat toy', 'chat')]
    for kw, animal in keywords:
        try:
            url = f"https://www.temu.com/api/poppy/v1/search?q={requests.utils.quote(kw)}&page=1&page_size=3"
            r = requests.get(url, headers=headers, timeout=12)
            if r.status_code != 200:
                continue
            data = r.json()
            items = data.get('result', {}).get('goods_list', [])
            for item in items[:2]:  # On prend les 2 premiers
                goods_id = str(item.get('goods_id', ''))
                name = item.get('goods_name', '')[:55]
                price_info = item.get('price_info', {})
                price = float(price_info.get('price', 0))
                original_price = float(price_info.get('original_price', price * 1.4))
                if not price or not name or not goods_id:
                    continue
                # Conversion approximative en DA (taux 145, arrondi à la centaine)
                np_da = round(price * 145 / 100) * 100
                op_da = round(original_price * 145 / 100) * 100 if original_price > price else round(np_da * 1.4 / 100) * 100
                if np_da < 500 or np_da > 50000:
                    continue
                link = f"https://www.temu.com/goods.html?goods_id={goods_id}"
                if TEMU_AFF_ID:
                    link += f"&refer_affiliate_id={TEMU_AFF_ID}"
                discount = round((1 - np_da / op_da) * 100)
                pid += 1
                cat = 'alimentation' if 'food' in kw else 'accessoire'
                emoji = '🥩' if 'food' in kw else '🎾'
                product = {
                    'id': pid,
                    'type': 'flash' if discount >= 30 else 'sale',
                    'animal': animal,
                    'cat': cat,
                    'name': name,
                    'src': 'Temu',
                    'plat': 'temu',
                    'op': op_da,
                    'np': np_da,
                    'end_hours': random.randint(4, 16) if discount >= 30 else None,
                    'link': link,
                    'desc': 'Disponible sur Temu.'
                }
                live.append(product)
            time.sleep(2)  # Pause pour ne pas surcharger l'API
        except Exception as e:
            print(f"Erreur lors de la récupération Temu pour {kw}: {e}")
    return live

def save_products(products):
    """Écrit le fichier products.json et le pousse sur GitHub."""
    data = {
        'products': products,
        'updated': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    }
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Commit et push via API GitHub (plus fiable que subprocess)
    if GITHUB_TOKEN:
        url = f"https://api.github.com/repos/{REPO}/contents/products.json"
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        # Lire le fichier actuel pour obtenir le sha (nécessaire pour mettre à jour)
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            sha = r.json()['sha']
        else:
            sha = None  # Le fichier n'existe pas encore

        with open('products.json', 'rb') as f:
            content = f.read()
        import base64
        encoded = base64.b64encode(content).decode('utf-8')

        commit_message = f"Auto-update products {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        data = {
            'message': commit_message,
            'content': encoded,
            'branch': BRANCH
        }
        if sha:
            data['sha'] = sha

        r = requests.put(url, headers=headers, json=data)
        if r.status_code in (200, 201):
            print("✅ products.json mis à jour sur GitHub")
        else:
            print(f"❌ Erreur GitHub: {r.status_code} - {r.text}")
    else:
        print("⚠️  GITHUB_TOKEN non défini, fichier sauvegardé localement.")

# ===== MAIN =====
if __name__ == '__main__':
    print("🔄 Récupération des produits Temu...")
    live_products = fetch_temu_products()
    all_products = BASE_PRODUCTS + live_products
    print(f"📦 Total produits: {len(all_products)} (dont {len(live_products)} live)")
    save_products(all_products)
