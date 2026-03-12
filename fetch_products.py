import requests, json, os, time, random

TEMU_AFF_ID = os.environ.get('TEMU_AFFILIATE_ID', '')
ALI_TRACKING_ID = os.environ.get('ALI_TRACKING_ID', '')

ALI_LINKS = [
    'https://s.click.aliexpress.com/e/_c3Qyu8yn',
    'https://s.click.aliexpress.com/e/_c4UF0X5V',
    'https://s.click.aliexpress.com/e/_c4DRN5YL',
]

STATIC = [
    {'id':1,'type':'flash','animal':'chien','cat':'alimentation','e':'🥩','name':'Royal Canin Medium Adult 15kg','src':'Temu','plat':'temu','op':6800,'np':4200,'end_hours':6,'link':'https://temu.to/k/e6c3s5aetpv','desc':'Croquettes premium chiens taille moyenne.'},
    {'id':2,'type':'flash','animal':'chat','cat':'alimentation','e':'🐟','name':'Purina Pro Plan Saumon 10kg','src':'Temu','plat':'temu','op':5200,'np':2900,'end_hours':8,'link':'https://temu.to/k/e6sv54vok7h','desc':'Aliment complet chats adultes.'},
    {'id':3,'type':'flash','animal':'chien','cat':'sante','e':'💊','name':'Antiparasitaire Spot-On x6','src':'Temu','plat':'temu','op':2800,'np':980,'end_hours':5,'link':'https://temu.to/k/ehntxv1jh73','desc':'Protection puces et tiques 4 semaines.'},
    {'id':4,'type':'flash','animal':'chat','cat':'accessoire','e':'🛏️','name':'Griffoir Arbre a Chat 4 Niveaux','src':'Temu','plat':'temu','op':3500,'np':1400,'end_hours':12,'link':'https://temu.to/k/efi1scl4z9v','desc':'Griffoirs sisal naturel. 4 plateformes.'},
    {'id':5,'type':'flash','animal':'chien','cat':'accessoire','e':'📡','name':'Collier GPS Tracker Chien','src':'Temu','plat':'temu','op':4200,'np':2100,'end_hours':7,'link':'https://temu.to/k/esl7kn0x2v7','desc':'GPS temps reel. Waterproof IP67.'},
    {'id':6,'type':'flash','animal':'chien','cat':'alimentation','e':'🥩','name':'Alimentation Premium Chien','src':'AliExpress','plat':'aliexpress','op':4800,'np':2200,'end_hours':10,'link':'https://s.click.aliexpress.com/e/_c3Qyu8yn','desc':'Nourriture complete chien adulte.'},
    {'id':7,'type':'flash','animal':'chat','cat':'alimentation','e':'🐟','name':'Nourriture Premium Chat 5kg','src':'AliExpress','plat':'aliexpress','op':3200,'np':1450,'end_hours':14,'link':'https://s.click.aliexpress.com/e/_c4UF0X5V','desc':'Aliment complet chat adulte.'},
    {'id':8,'type':'sale','animal':'chien','cat':'accessoire','e':'🎾','name':'Kit Accessoires Animaux','src':'AliExpress','plat':'aliexpress','op':2600,'np':980,'end_hours':None,'link':'https://s.click.aliexpress.com/e/_c4DRN5YL','desc':'Accessoires complets. Livraison 15-25j.'},
    {'id':9,'type':'sale','animal':'chat','cat':'hygiene','e':'🧴','name':'Shampoing Demelant Poils Longs','src':'Temu','plat':'temu','op':980,'np':390,'end_hours':None,'link':'https://temu.to/k/efi1scl4z9v','desc':'Formule douce sans parabenes.'},
    {'id':10,'type':'sale','animal':'chien','cat':'sante','e':'🦷','name':'Kit Hygiene Dentaire Veterinaire','src':'Temu','plat':'temu','op':1200,'np':620,'end_hours':None,'link':'https://temu.to/k/esl7kn0x2v7','desc':'Previent le tartre.'},
    {'id':11,'type':'sale','animal':'chat','cat':'accessoire','e':'🏠','name':'Maison Transport Rigide Taille M','src':'Temu','plat':'temu','op':3800,'np':1650,'end_hours':None,'link':'https://temu.to/k/efi1scl4z9v','desc':'Verrou securise, ventilation optimale.'},
    {'id':12,'type':'sale','animal':'chien','cat':'hygiene','e':'🛁','name':'Table Toilettage Pliable Pro','src':'Temu','plat':'temu','op':8500,'np':4200,'end_hours':None,'link':'https://temu.to/k/e6c3s5aetpv','desc':'Table pliable bras de retenue.'},
]

def fetch_temu(keywords):
    products = []
    headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36','Accept':'application/json'}
    pid = 200
    for keyword, animal in keywords:
        try:
            url = f"https://www.temu.com/api/poppy/v1/search?q={requests.utils.quote(keyword)}&page=1&page_size=4"
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code != 200: continue
            items = r.json().get('result',{}).get('goods_list',[])
            for item in items[:2]:
                item_id = str(item.get('goods_id',''))
                name = item.get('goods_name','')[:55]
                pi = item.get('price_info',{})
                pr = float(pi.get('price',0))
                op = float(pi.get('original_price', pr*1.4))
                if not pr or not name: continue
                np_ = round(pr*145/100)*100
                op_ = round(op*145/100)*100 if op>pr else round(np_*1.4/100)*100
                if np_<500 or np_>50000: continue
                link = f"https://www.temu.com/goods.html?goods_id={item_id}"
                if TEMU_AFF_ID: link += f"&refer_affiliate_id={TEMU_AFF_ID}"
                disc = round((1-np_/op_)*100)
                pid += 1
                products.append({'id':pid,'type':'flash' if disc>=30 else 'sale','animal':animal,'cat':'alimentation' if 'food' in keyword else 'accessoire','e':'🥩' if 'food' in keyword else '🐾','name':name,'src':'Temu','plat':'temu','op':op_,'np':np_,'end_hours':random.randint(4,18) if disc>=30 else None,'link':link,'desc':'Disponible sur Temu.'})
            time.sleep(1)
        except Exception as e:
            print(f"Temu error: {e}")
    return products

if __name__ == '__main__':
    print("Fetching...")
    live = fetch_temu([('dog food','chien'),('cat food','chat'),('dog toy','chien'),('cat tree','chat')])
    all_p = STATIC + live if live else STATIC
    with open('products.json','w',encoding='utf-8') as f:
        json.dump({'products':all_p,'updated':time.strftime('%Y-%m-%dT%H:%M:%SZ')},f,ensure_ascii=False,indent=2)
    print(f"{len(all_p)} products saved.")
