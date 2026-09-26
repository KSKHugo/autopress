#!/usr/bin/env python3
"""Writes the Coastline Journal demo folder and the mock's terms for one language.
   python3 demo.py <lang> <outdir>   → <outdir>/Coastline Journal/…, <outdir>/terms.json"""
import json, os, shutil, sys

D = {
"en": dict(about="About Coastline Journal", algarve="Walking the Algarve Cliffs", lisbon="Lisbon in Three Days",
  excerpt="Seven hills, one tram line and the best custard tarts in town. A long weekend, hour by hour.",
  tags=["Lisbon", "City trips", "Food"], portugal="Portugal", guides="Guides",
  alt="The rooftops of the Alfama at sunset", seo="Lisbon in Three Days: A Long-Weekend Itinerary",
  meta="A three-day Lisbon itinerary with the Alfama, Belém and the best custard tarts, hour by hour, with costs.",
  focus="Lisbon in three days", newsletter="September Letter: Harvest on the Douro", packing="The Carry-on Packing List",
  porto="Porto by Tram", sintra="A Day in Sintra",
  cats=["Spain", "France", "Slow travel", "Food & Wine", "Rail", "Islands"],
  more=["Porto", "Hiking", "Algarve", "Planning", "Trams", "Beaches", "Museums", "Coffee", "Sintra", "Day trips", "Budget", "Wine"]),
"de": dict(about="Über Coastline Journal", algarve="Wandern an den Klippen der Algarve", lisbon="Lissabon in drei Tagen",
  excerpt="Sieben Hügel, eine Straßenbahnlinie und die besten Puddingtörtchen der Stadt. Ein langes Wochenende, Stunde für Stunde.",
  tags=["Lissabon", "Städtereisen", "Essen"], portugal="Portugal", guides="Reiseführer",
  alt="Die Dächer der Alfama bei Sonnenuntergang", seo="Lissabon in drei Tagen: ein Wochenend-Reiseplan",
  meta="Ein Reiseplan für drei Tage Lissabon mit Alfama, Belém und den besten Pastéis de Nata, Stunde für Stunde, mit Kosten.",
  focus="Lissabon in drei Tagen", newsletter="Septemberbrief: Weinlese am Douro", packing="Die Handgepäck-Packliste",
  porto="Porto mit der Straßenbahn", sintra="Ein Tag in Sintra",
  cats=["Spanien", "Frankreich", "Langsam reisen", "Essen & Wein", "Bahn", "Inseln"],
  more=["Porto", "Wandern", "Algarve", "Planung", "Straßenbahn", "Strände", "Museen", "Kaffee", "Sintra", "Tagesausflüge", "Budget", "Wein"]),
"fr": dict(about="À propos de Coastline Journal", algarve="Marcher sur les falaises de l'Algarve", lisbon="Lisbonne en trois jours",
  excerpt="Sept collines, une ligne de tram et les meilleurs pastéis de la ville. Un long week-end, heure par heure.",
  tags=["Lisbonne", "Escapades urbaines", "Gastronomie"], portugal="Portugal", guides="Guides",
  alt="Les toits de l'Alfama au coucher du soleil", seo="Lisbonne en trois jours : un itinéraire de week-end",
  meta="Un itinéraire de trois jours à Lisbonne : Alfama, Belém et les meilleurs pastéis de nata, heure par heure, avec les coûts.",
  focus="Lisbonne en trois jours", newsletter="Lettre de septembre : les vendanges du Douro", packing="La liste du bagage cabine",
  porto="Porto en tramway", sintra="Une journée à Sintra",
  cats=["Espagne", "France", "Voyage lent", "Vins & gastronomie", "Train", "Îles"],
  more=["Porto", "Randonnée", "Algarve", "Préparatifs", "Tramway", "Plages", "Musées", "Café", "Sintra", "Excursions", "Budget", "Vin"]),
"es": dict(about="Sobre Coastline Journal", algarve="Caminando por los acantilados del Algarve", lisbon="Lisboa en tres días",
  excerpt="Siete colinas, una línea de tranvía y los mejores pasteles de nata de la ciudad. Un fin de semana largo, hora a hora.",
  tags=["Lisboa", "Escapadas urbanas", "Gastronomía"], portugal="Portugal", guides="Guías",
  alt="Los tejados de la Alfama al atardecer", seo="Lisboa en tres días: itinerario de fin de semana",
  meta="Un itinerario de tres días por Lisboa con la Alfama, Belém y los mejores pasteles de nata, hora a hora, con costes.",
  focus="Lisboa en tres días", newsletter="Carta de septiembre: vendimia en el Duero", packing="La lista del equipaje de mano",
  porto="Oporto en tranvía", sintra="Un día en Sintra",
  cats=["España", "Francia", "Viaje lento", "Comida y vino", "Tren", "Islas"],
  more=["Oporto", "Senderismo", "Algarve", "Planificación", "Tranvías", "Playas", "Museos", "Café", "Sintra", "Excursiones", "Presupuesto", "Vino"]),
"it": dict(about="Chi è Coastline Journal", algarve="A piedi sulle scogliere dell'Algarve", lisbon="Lisbona in tre giorni",
  excerpt="Sette colli, una linea di tram e i migliori pastéis della città. Un weekend lungo, ora per ora.",
  tags=["Lisbona", "Città", "Cibo"], portugal="Portogallo", guides="Guide",
  alt="I tetti dell'Alfama al tramonto", seo="Lisbona in tre giorni: itinerario per un weekend",
  meta="Un itinerario di tre giorni a Lisbona con l'Alfama, Belém e i migliori pastéis de nata, ora per ora, con i costi.",
  focus="Lisbona in tre giorni", newsletter="Lettera di settembre: la vendemmia sul Douro", packing="La lista del bagaglio a mano",
  porto="Porto in tram", sintra="Una giornata a Sintra",
  cats=["Spagna", "Francia", "Viaggi lenti", "Cibo e vino", "Treno", "Isole"],
  more=["Porto", "Escursioni", "Algarve", "Preparativi", "Tram", "Spiagge", "Musei", "Caffè", "Sintra", "Gite", "Budget", "Vino"]),
"pt": dict(about="Sobre o Coastline Journal", algarve="A pé pelas falésias do Algarve", lisbon="Lisboa em três dias",
  excerpt="Sete colinas, uma linha de elétrico e os melhores pastéis de nata da cidade. Um fim de semana prolongado, hora a hora.",
  tags=["Lisboa", "Escapadinhas", "Gastronomia"], portugal="Portugal", guides="Guias",
  alt="Os telhados de Alfama ao pôr do sol", seo="Lisboa em três dias: roteiro de fim de semana",
  meta="Um roteiro de três dias em Lisboa com Alfama, Belém e os melhores pastéis de nata, hora a hora, com custos.",
  focus="Lisboa em três dias", newsletter="Carta de setembro: vindimas no Douro", packing="A lista da bagagem de mão",
  porto="O Porto de elétrico", sintra="Um dia em Sintra",
  cats=["Espanha", "França", "Viagem lenta", "Comida e vinho", "Comboio", "Ilhas"],
  more=["Porto", "Caminhadas", "Algarve", "Planeamento", "Elétricos", "Praias", "Museus", "Café", "Sintra", "Passeios", "Orçamento", "Vinho"]),
"nl": dict(about="Over Coastline Journal", algarve="Wandelen langs de kliffen van de Algarve", lisbon="Lissabon in drie dagen",
  excerpt="Zeven heuvels, één tramlijn en de beste pasteitjes van de stad. Een lang weekend, uur voor uur.",
  tags=["Lissabon", "Stedentrips", "Eten"], portugal="Portugal", guides="Gidsen",
  alt="De daken van de Alfama bij zonsondergang", seo="Lissabon in drie dagen: een weekendroute",
  meta="Een driedaagse route door Lissabon met de Alfama, Belém en de beste pastéis de nata, uur voor uur, met kosten.",
  focus="Lissabon in drie dagen", newsletter="Septemberbrief: druivenoogst aan de Douro", packing="De paklijst voor handbagage",
  porto="Porto per tram", sintra="Een dag in Sintra",
  cats=["Spanje", "Frankrijk", "Langzaam reizen", "Eten & wijn", "Trein", "Eilanden"],
  more=["Porto", "Wandelen", "Algarve", "Planning", "Trams", "Stranden", "Musea", "Koffie", "Sintra", "Dagtochten", "Budget", "Wijn"]),
"ja": dict(about="Coastline Journal について", algarve="アルガルヴェの断崖を歩く", lisbon="リスボン3日間",
  excerpt="7つの丘、1本の路面電車、街いちばんのエッグタルト。週末をたっぷり、1時間ごとに。",
  tags=["リスボン", "街歩き", "グルメ"], portugal="ポルトガル", guides="ガイド",
  alt="夕暮れのアルファマの屋根", seo="リスボン3日間：週末の旅程",
  meta="アルファマ、ベレン、最高のエッグタルトをめぐるリスボン3日間の旅程。1時間ごと、費用つき。",
  focus="リスボン 3日間", newsletter="9月の便り：ドウロのぶどう収穫", packing="機内持ち込みの持ち物リスト",
  porto="路面電車でめぐるポルト", sintra="シントラの1日",
  cats=["スペイン", "フランス", "スローな旅", "食とワイン", "鉄道", "島"],
  more=["ポルト", "ハイキング", "アルガルヴェ", "旅の準備", "路面電車", "ビーチ", "美術館", "コーヒー", "シントラ", "日帰り旅行", "予算", "ワイン"]),
"zh": dict(about="关于 Coastline Journal", algarve="漫步阿尔加维海崖", lisbon="里斯本三日游",
  excerpt="七座山丘、一条电车线路和城里最好吃的蛋挞。一个长周末，按小时安排。",
  tags=["里斯本", "城市旅行", "美食"], portugal="葡萄牙", guides="指南",
  alt="日落时分阿尔法玛的屋顶", seo="里斯本三日游：周末行程",
  meta="里斯本三日行程：阿尔法玛、贝伦和最好的葡式蛋挞，按小时安排，附费用。",
  focus="里斯本三日游", newsletter="九月来信：杜罗河谷的葡萄收获", packing="登机箱打包清单",
  porto="乘电车游波尔图", sintra="辛特拉一日",
  cats=["西班牙", "法国", "慢旅行", "美食与葡萄酒", "铁路", "海岛"],
  more=["波尔图", "徒步", "阿尔加维", "行前准备", "电车", "海滩", "博物馆", "咖啡", "辛特拉", "一日游", "预算", "葡萄酒"]),
}

lang, out = sys.argv[1], sys.argv[2]
t = D[lang]
src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(out))), "demo", "Coastline Journal")
dst = os.path.join(out, "Coastline Journal")
shutil.rmtree(dst, ignore_errors=True)
os.makedirs(os.path.join(dst, "images"))
for name in os.listdir(src):
    if name.endswith(".jpg"):
        shutil.copy(os.path.join(src, name), dst)
for name in os.listdir(os.path.join(src, "images")):
    shutil.copy(os.path.join(src, "images", name), os.path.join(dst, "images"))
L = lambda items: "[" + ", ".join(items) + "]"
docs = {
"lisbon-in-three-days.md": f"""---
title: {t['lisbon']}
type: post
status: draft
slug: lisbon-in-three-days
excerpt: {t['excerpt']}
tags: {L(t['tags'])}
categories: {t['portugal']}
featured_image_alt: {t['alt']}
credit: © Maria Santos
seo_title: {t['seo']}
meta_description: {t['meta']}
focus_keyword: {t['focus']}
---

# {t['lisbon']}

Lisbon rewards people who walk.

![{t['alt']}](images/alfama-rooftops.jpg)

| Stop | Time |
|------|------|
| Castelo de São Jorge | 2 h |
""",
"porto-by-tram.md": f"""---
title: {t['porto']}
status: scheduled
date: 2026-10-03 08:30
tags: {L([t['more'][0], t['tags'][1], t['more'][4]])}
categories: {t['portugal']}
credit: © Maria Santos
---

# {t['porto']}

![Douro](images/douro-valley.jpg)
""",
"algarve-cliffs.md": f"""---
title: {t['algarve']}
status: publish
tags: {L([t['more'][2], t['more'][1], t['more'][5]])}
categories: {t['portugal']}
credit: © Maria Santos
---

# {t['algarve']}
""",
"sintra-palace.md": f"""---
title: {t['sintra']}
status: scheduled
date: 2026-10-05 08:30
tags: {L([t['more'][8], t['more'][9]])}
categories: {t['portugal']}
---

# {t['sintra']}
""",
"packing-list.md": f"""---
title: {t['packing']}
status: draft
tags: {L([t['more'][3], t['more'][10]])}
categories: {t['guides']}
---

# {t['packing']}
""",
"about.md": f"""---
title: {t['about']}
type: page
status: draft
slug: about
---

# {t['about']}
""",
"newsletter-september.md": f"""# {t['newsletter']}

![Douro](images/douro-valley.jpg)
""",
}
for name, text in docs.items():
    with open(os.path.join(dst, name), "w") as f:
        f.write(text)
cats = [t["guides"]] + t["cats"] + [t["portugal"]]
terms = {"categories": {c.replace("&", "&amp;"): 11 + i for i, c in enumerate(cats)},
         "tags": {c: 30 + i for i, c in enumerate(t["more"] + t["tags"])}}
json.dump(terms, open(os.path.join(out, "terms.json"), "w"), ensure_ascii=False)
print("demo for", lang, "in", dst)
