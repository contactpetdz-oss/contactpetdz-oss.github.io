import requests, json, time, random, os, subprocess

TOKEN = open(os.path.expanduser("~/.petdz_token")).read().strip()
REPO = "https://" + TOKEN + "@github.com/contactpetdz-oss/contactpetdz-oss.github.io.git"

ALI_LINKS = [
    'https://s.click.aliexpress.com/e/_c3Qyu8yn',
    'https://s.click.aliexpress.com/e/_c4UF0X5V',
    'https://s.click.aliexpress.com/e/_c4DRN5YL',
]

BASE_PRODUCTS = [
    {'id':1,'type':'flash','animal':'chien','cat':'alimentation','e':'🥩','name':'Royal Canin Medium Adult 15kg','src':'Temu','plat':'temu','op':6800,'np':4200,'end_hours':6,'link':'https://temu.to/k/e6c3s5aetpv','desc':'Croquettes premium chiens.'},
    {'id':2,'type':'flash','animal':'chat','cat':'alimentation','e':'🐟','name':'Purina Pro Plan Saumon 10kg','src':'Temu','plat':'temu','op':5200,'np':2900,'end_hours':8,'link':'https://temu.to/k/e6sv54vok7h','desc':'Aliment complet chats adultes.'},
    {'id':3,'type':'flash','animal':'chien','cat':'sante','e':'💊','name':'Antiparasitaire Spot-On x6','src':'Temu','plat':'temu','op':2800,'np':980,'end_hours':5,'link':'https://temu.to/k/ehntxv1jh73','desc':'Protection puces et tiques.'},
    {'id':4,'type':'flash','animal':'chat','cat':'accessoire','e':'🛏️','name':'Griffoir Arbre a Chat 4 Niveaux','src':'Temu','plat':'temu','op':3500,'np':1400,'end_hours':12,'link':'https://temu.to/k/efi1scl4z9v','desc':'Griffoirs sisal naturel.'},
    {'id':5,'type':'flash','animal':'chien','cat':'accessoire','e':'📡','name':'Collier GPS Tracker Chien','src':'Temu','plat':'temu','op':4200,'np':2100,'end_hours':7,'link':'https://temu.to/k/esl7kn0x2v7','desc':'GPS temps reel. Waterproof IP67.'},
    {'id':6,'type':'flash','animal':'chien','cat':'alimentation','e':'🥩','name':'Alimentation Premium Chien','src':'AliExpress','plat':'aliexpress','op':4800,'np':2200,'end_hours':10,'link':ALI_LINKS[0],'desc':'Nourriture complete chien adulte.'},
    {'id':7,'type':'flash','animal':'chat','cat':'alimentation','e':'🐟','name':'Nourriture Premium Chat 5kg','src':'AliExpress','plat':'aliexpress','op':3200,'np':1450,'end_hours':14,'link':ALI_LINKS[1],'desc':'Aliment complet chat adulte.'},
    {'id':8,'type':'sale','animal':'chien','cat':'accessoire','e':'🎾','name':'Kit Accessoires Animaux','src':'AliExpress','plat':'aliexpress','op':2600,'np':980,'end_hours':None,'link':ALI_LINKS[2],'desc':'Accessoires complets.'},
    {'id':9,'type':'sale','animal':'chat','cat':'hygiene','e':'🧴','name':'Shampoing Demelant Poils Longs','src':'Temu','plat':'temu','op':980,'np':390,'end_hours':None,'link':'https://temu.to/k/efi1scl4z9v','desc':'Formule douce.'},
    {'id':10,'type':'sale','animal':'chien','cat':'sante','e':'🦷','name':'Kit Hygiene Dentaire Veterinaire','src':'Temu','plat':'temu','op':1200,'np':620,'end_hours':None,'link':'https://temu.to/k/esl7kn0x2v7','desc':'Previent le tartre.'},
    {'id':11,'type':'sale','animal':'chat','cat':'accessoire','e':'🏠','name':'Maison Transport Rigide Taille M','src':'Temu','plat':'temu','op':3800,'np':1650,'end_hours':None,'link':'https://temu.to/k/efi1scl4z9v','desc':'Verrou securise.'},
    {'id':12,'type':'sale','animal':'chien','cat':'hygiene','e':'🛁','name':'Table Toilettage Pliable Pro','src':'Temu','plat':'temu','op':8500,'np':4200,'end_hours':None,'link':'https://temu.to/k/e6c3s5aetpv','desc':'Table pliable pro.'},
]

def fetch_temu():
    live = []
    headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36'}
    pid = 200
    for kw, animal in [('dog food','chien'),('cat food','chat'),('dog toy','chien'),('cat toy','chat')]:
        try:
            r = requests.get(f"https://www.temu.com/api/poppy/v1/search?q={kw}&page=1&page_size=3", headers=headers, timeout=12)
            if r.status_code != 200: continue
            items = r.json().get('result',{}).get('goods_list',[])
            for item in items[:2]:
                gid = str(item.get('goods_id',''))
                name = item.get('goods_name','')[:55]
                pi = item.get('price_info',{})
                pr = float(pi.get('price',0))
                op = float(pi.get('original_price', pr*1.4))
                if not pr or not name or not gid: continue
                np_ = round(pr*145/100)*100
                op_ = round(op*145/100)*100 if op>pr else round(np_*1.4/100)*100
                if np_<500 or np_>50000: continue
                link = f"https://www.temu.com/goods.html?goods_id={gid}"
                disc = round((1-np_/op_)*100)
                pid += 1
                live.append({'id':pid,'type':'flash' if disc>=30 else 'sale','animal':animal,'cat':'alimentation' if 'food' in kw else 'accessoire','e':'🥩' if 'food' in kw else '🎾','name':name,'src':'Temu','plat':'temu','op':op_,'np':np_,'end_hours':random.randint(4,16) if disc>=30 else None,'link':link,'desc':'Disponible sur Temu.'})
            time.sleep(2)
        except Exception as e:
            print(f"Temu error: {e}")
    return live

print("Fetching products...")
live = fetch_temu()
all_p = BASE_PRODUCTS + live
print(f"{len(all_p)} products total ({len(live)} live from Temu)")

with open('products.json','w',encoding='utf-8') as f:
    json.dump({'products':all_p,'updated':time.strftime('%Y-%m-%dT%H:%M:%SZ')},f,ensure_ascii=False,indent=2)

os.system('git add products.json')
os.system(f'git commit -m "Auto-update {time.strftime("%Y-%m-%d %H:%M")}"')
result = os.system(f'git push {REPO} main')
if result == 0:
    print("GitHub updated successfully.")
else:
    print("Push failed.")
