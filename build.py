#!/usr/bin/env python3
"""Builds the page in every language from one template.

    python3 build.py

template.html holds the structure, the dictionaries below hold the words. English is
the primary language and lands in index.html; every other language gets its own folder.
A new language = one more dictionary.
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
SITE = "https://hybrid-autopress.com/"

EN = {
    "lang": "en", "path": "", "root": "",
    "other_lang_name": "Deutsch", "other_lang_href": "de/", "other_lang_code": "de",
    "title": "Hybrid AutoPress: Markdown to WordPress, many files at once",
    "description": "Hybrid AutoPress uploads many Markdown files to WordPress in one go: as posts or pages, as drafts or published, images included. For iPhone, iPad and Mac.",
    "skip": "Skip to content",
    "nav_how": "How it works", "nav_images": "Images", "nav_sites": "Your WordPress", "nav_benefits": "Benefits",
    "hero_eyebrow": "For iPhone, iPad and Mac",
    "hero_h1": 'A folder of Markdown in. <span class="hl">A WordPress site out.</span>',
    "hero_lede": "Hybrid AutoPress uploads many Markdown files to WordPress in one go. Every file becomes a post or a page, with headings, links, lists, tables and images, saved as a draft or published right away.",
    "soon": "Coming soon to the App Store",
    "hero_more": "See how it works",
    "hero_alt": "Hybrid AutoPress on the Mac: seven Markdown documents in the list, the post “Lisbon in Three Days” with its featured image, slug, excerpt, categories and tags.",

    "step": "Step",
    "s1_h": "Add files. Or a whole folder.",
    "s1_p": "Pick single files, choose a folder including its subfolders, or drag everything into the window. AutoPress reads each title from the front matter, the first heading or the file name.",
    "s1_alt": "The document list on the Mac with seven Markdown files, each marked as post or page.",
    "s2_h": "Decide once. Adjust where needed.",
    "s2_p": "Post or page, draft or live: set it once for all documents and override it for any single one. Before anything is published immediately, AutoPress asks once.",
    "s2_alt": "The post “Walking the Algarve Cliffs” is set to “Publish now”, while all other documents stay drafts.",
    "s3_h": "Press upload. Watch it go.",
    "s3_p": "One document after the other is created in WordPress, its images first. A progress bar shows how far along you are, and you can stop at any time.",
    "s3_alt": "An upload in progress: two of seven documents are done, one is being created in WordPress, the rest are waiting.",
    "s4_h": "Done. With a link back.",
    "s4_p": "Every finished document gets a green check mark and a link to view it on the site or to keep editing in WordPress. If something fails, AutoPress tells you why and what to do about it.",
    "s4_alt": "All seven documents carry a green check mark; the selected one offers “View” and “Edit in WordPress”.",

    "img_eyebrow": "Images",
    "img_h": 'Your pictures <span class="hl">come along.</span>',
    "img_lede": "No more uploading images by hand and patching links. What lies next to your Markdown file arrives in WordPress with it.",
    "img_1_t": "Into the media library", "img_1_p": "Local images in the text are uploaded with their alt text and linked in the post. Each one goes up only once per site and session.",
    "img_2_t": "Featured image, found automatically", "img_2_p": "Name it in the front matter, or put a picture with the same name next to the file: lisbon.md → lisbon.jpg. Or pick a file or a photo.",
    "img_3_t": "HEIC and TIFF become JPEG", "img_3_p": "Photos straight from the iPhone are converted on the way, so every browser can show them.",
    "img_alt": "Hybrid AutoPress on the iPhone: a post with its automatically found featured image, slug and excerpt.",

    "dev_eyebrow": "One app, three devices",
    "dev_h": 'At your desk. <span class="hl">Or on the sofa.</span>',
    "dev_lede": "The same app on iPhone, iPad and Mac. Upload from wherever your files are: iCloud Drive, the Files app or a folder on your Mac.",
    "ipad_alt": "Hybrid AutoPress on the iPad: all seven documents uploaded, the selected post saved as a draft.",
    "iphone_alt": "Hybrid AutoPress on the iPhone: the list of documents with the button “Upload 7 Documents”.",

    "fm_eyebrow": "Front matter",
    "fm_h": 'A few lines on top. <span class="hl">If you like.</span>',
    "fm_lede": "Optional front matter controls everything per file. Without it, the first heading becomes the title and does not show up twice in the post.",
    "fm_1_t": "Everything WordPress needs", "fm_1_p": "title, type, status, slug, excerpt, date, tags, categories, featured_image.",
    "fm_2_t": "Tags and categories are created", "fm_2_p": "What does not exist on the site yet is added during the upload.",
    "fm_3_t": "Clean HTML", "fm_3_p": "Headings, links, lists, real tables and quotes, converted by the engine that also drives Hybrid.",
    "code_c1": "# optional: every line may be left out",
    "code_body": "Lisbon rewards people who walk …",

    "site_eyebrow": "Your WordPress",
    "site_h": 'Works with your WordPress. <span class="hl">Wherever it is hosted.</span>',
    "site_lede": "Sign in through the browser and WordPress itself creates an application password for the app. Or enter one by hand. The REST API is found automatically. WordPress.com sites connect by signing in through the browser.",
    "hosts_more": "… and any other host",
    "c1_t": "Credentials stay in the keychain", "c1_p": "Never in the settings, never in a file. And only over https: credentials are not sent over an unencrypted connection.",
    "c2_t": "Errors with a way out", "c2_p": "If your server swallows the <code>Authorization</code> header, which is common with shared hosting, AutoPress recognises it and shows the <code>.htaccess</code> line that fixes it.",
    "c3_t": "Talks to your site, nothing else", "c3_p": "No account needed, no tracking, no server in between. The app speaks directly to your WordPress.",

    "ben_eyebrow": "What you get out of it",
    "ben_h": 'Less clicking. <span class="hl">More publishing.</span>',
    "b1_big": "1×", "b1_t": "One click instead of twenty rounds", "b1_p": "Twenty articles no longer mean twenty times copy, paste, upload images, fix links. Add the folder, press upload.",
    "b2_t": "Drafts first", "b2_p": "Everything can arrive as a draft. Check it in WordPress and publish when you are happy with it.",
    "b3_t": "Your text stays yours", "b3_p": "The Markdown files on your disk remain the original, readable in any editor, today and in ten years.",
    "b4_t": "Made for AI workflows", "b4_p": "Texts from ChatGPT, Claude and the like arrive as Markdown anyway. AutoPress takes them to your site without detours.",
    "b5_t": "For whole sites, too", "b5_p": "Moving a site or starting a new one? Pages and posts go up in a single run, tags and categories included.",
    "sis_t": "From the maker of Hybrid", "sis_p": "Hybrid is the Markdown editor that knows who wrote what: you, an AI or a source. AutoPress takes what you write there to WordPress.",
    "sis_link": "Discover Hybrid",

    "end_h": 'Write in Markdown. <span class="hl">Publish in bulk.</span>',
    "end_lede": "Hybrid AutoPress is coming to the App Store: one app for iPhone, iPad and Mac.",
    "req": "Requires iOS 17, iPadOS 17 or macOS 14 · English and German",
    "foot_imprint": "Legal Notice (Impressum)", "foot_privacy": "Privacy Policy", "foot_hybrid": "Hybrid Editor",
    "foot_imprint_href": "impressum/", "foot_privacy_href": "datenschutz/",
    "foot_hybrid_href": "https://hybrid-editor.com/",
    "fine": "WordPress is a trademark of the WordPress Foundation. Hybrid AutoPress is an independent app and is not affiliated with or endorsed by the WordPress Foundation, Automattic or any of the hosting companies named. Apple, iPhone, iPad, Mac and App Store are trademarks of Apple Inc. The screenshots show sample content.",
}

DE = dict(EN, **{
    "lang": "de", "path": "de/", "root": "../",
    "other_lang_name": "English", "other_lang_href": "../", "other_lang_code": "en",
    "title": "Hybrid AutoPress: Markdown zu WordPress, viele Dateien auf einmal",
    "description": "Hybrid AutoPress lädt viele Markdown-Dateien auf einmal zu WordPress hoch: als Beiträge oder Seiten, als Entwurf oder veröffentlicht, mit allen Bildern. Für iPhone, iPad und Mac.",
    "skip": "Zum Inhalt springen",
    "nav_how": "So geht’s", "nav_images": "Bilder", "nav_sites": "Dein WordPress", "nav_benefits": "Vorteile",
    "hero_eyebrow": "Für iPhone, iPad und Mac",
    "hero_h1": 'Ein Ordner Markdown rein. <span class="hl">Eine WordPress-Website raus.</span>',
    "hero_lede": "Hybrid AutoPress lädt viele Markdown-Dateien auf einmal zu WordPress hoch. Aus jeder Datei wird ein Beitrag oder eine Seite, mit Überschriften, Links, Listen, Tabellen und Bildern, als Entwurf oder sofort veröffentlicht.",
    "soon": "Bald im App Store",
    "hero_more": "So funktioniert es",
    "hero_alt": "Hybrid AutoPress auf dem Mac: sieben Markdown-Dokumente in der Liste, der Beitrag „Lisbon in Three Days“ mit Beitragsbild, Slug, Auszug, Kategorien und Schlagwörtern.",

    "step": "Schritt",
    "s1_h": "Dateien hinzufügen. Oder gleich den Ordner.",
    "s1_p": "Einzelne Dateien wählen, einen Ordner samt Unterordnern oder alles ins Fenster ziehen. Den Titel liest AutoPress aus dem Front Matter, der ersten Überschrift oder dem Dateinamen.",
    "s1_alt": "Die Dokumentliste auf dem Mac mit sieben Markdown-Dateien, jede als Beitrag oder Seite markiert.",
    "s2_h": "Einmal entscheiden. Wo nötig abweichen.",
    "s2_p": "Beitrag oder Seite, Entwurf oder live: einmal für alle Dokumente einstellen und bei jedem einzelnen abweichen. Bevor etwas sofort veröffentlicht wird, fragt AutoPress ein Mal nach.",
    "s2_alt": "Der Beitrag „Walking the Algarve Cliffs“ steht auf „Publish now“, alle anderen Dokumente bleiben Entwürfe.",
    "s3_h": "Hochladen. Und zusehen.",
    "s3_p": "Ein Dokument nach dem anderen entsteht in WordPress, die Bilder zuerst. Ein Fortschrittsbalken zeigt, wie weit du bist, und anhalten geht jederzeit.",
    "s3_alt": "Ein laufender Upload: zwei von sieben Dokumenten sind fertig, eines wird in WordPress angelegt, die übrigen warten.",
    "s4_h": "Fertig. Mit Link zurück.",
    "s4_p": "Jedes fertige Dokument bekommt einen grünen Haken und einen Link zur Ansicht auf der Website oder zum Weiterbearbeiten in WordPress. Geht etwas schief, sagt AutoPress, woran es liegt und was hilft.",
    "s4_alt": "Alle sieben Dokumente tragen einen grünen Haken; das ausgewählte bietet „View“ und „Edit in WordPress“.",

    "img_eyebrow": "Bilder",
    "img_h": 'Deine Bilder <span class="hl">kommen mit.</span>',
    "img_lede": "Schluss mit Bildern von Hand hochladen und Links flicken. Was neben der Markdown-Datei liegt, kommt mit ihr in WordPress an.",
    "img_1_t": "Ab in die Mediathek", "img_1_p": "Lokale Bilder im Text werden mit ihrem Alt-Text hochgeladen und im Beitrag verknüpft, jedes pro Website und Sitzung nur ein Mal.",
    "img_2_t": "Beitragsbild, automatisch gefunden", "img_2_p": "Im Front Matter nennen oder ein gleichnamiges Bild neben die Datei legen: lissabon.md → lissabon.jpg. Oder eine Datei bzw. ein Foto auswählen.",
    "img_3_t": "HEIC und TIFF werden zu JPEG", "img_3_p": "Fotos direkt vom iPhone werden unterwegs umgewandelt, damit jeder Browser sie anzeigt.",
    "img_alt": "Hybrid AutoPress auf dem iPhone: ein Beitrag mit automatisch gefundenem Beitragsbild, Slug und Auszug.",

    "dev_eyebrow": "Eine App, drei Geräte",
    "dev_h": 'Am Schreibtisch. <span class="hl">Oder auf dem Sofa.</span>',
    "dev_lede": "Dieselbe App auf iPhone, iPad und Mac. Lade von dort hoch, wo deine Dateien liegen: iCloud Drive, die Dateien-App oder ein Ordner auf dem Mac.",
    "ipad_alt": "Hybrid AutoPress auf dem iPad: alle sieben Dokumente hochgeladen, der ausgewählte Beitrag als Entwurf gesichert.",
    "iphone_alt": "Hybrid AutoPress auf dem iPhone: die Dokumentliste mit der Taste „Upload 7 Documents“.",

    "fm_eyebrow": "Front Matter",
    "fm_h": 'Ein paar Zeilen obendrauf. <span class="hl">Wenn du magst.</span>',
    "fm_lede": "Optionales Front Matter steuert alles pro Datei. Ohne wird die erste Überschrift zum Titel und steht dann nicht doppelt im Beitrag.",
    "fm_1_t": "Alles, was WordPress braucht", "fm_1_p": "title, type, status, slug, excerpt, date, tags, categories, featured_image.",
    "fm_2_t": "Schlagwörter und Kategorien entstehen mit", "fm_2_p": "Was es auf der Website noch nicht gibt, wird beim Upload angelegt.",
    "fm_3_t": "Sauberes HTML", "fm_3_p": "Überschriften, Links, Listen, echte Tabellen und Zitate, umgewandelt von der Technik, die auch in Hybrid steckt.",
    "code_c1": "# optional: jede Zeile darf fehlen",

    "site_eyebrow": "Dein WordPress",
    "site_h": 'Läuft mit deinem WordPress. <span class="hl">Egal, wo es gehostet ist.</span>',
    "site_lede": "Im Browser anmelden, und WordPress legt selbst ein Anwendungspasswort für die App an. Oder du trägst eines von Hand ein. Die REST-API wird automatisch gefunden. Websites bei WordPress.com verbindest du per Anmeldung im Browser.",
    "hosts_more": "… und jeder andere Anbieter",
    "c1_t": "Zugangsdaten bleiben im Schlüsselbund", "c1_p": "Nie in den Einstellungen, nie in einer Datei. Und nur über https: Über eine unverschlüsselte Verbindung werden keine Zugangsdaten gesendet.",
    "c2_t": "Fehler mit Ausweg", "c2_p": "Verschluckt dein Server den <code>Authorization</code>-Header, was bei Shared Hosting häufig vorkommt, erkennt AutoPress das und zeigt die passende <code>.htaccess</code>-Zeile.",
    "c3_t": "Spricht mit deiner Website, sonst mit niemandem", "c3_p": "Kein Konto nötig, kein Tracking, kein Server dazwischen. Die App redet direkt mit deinem WordPress.",

    "ben_eyebrow": "Was du davon hast",
    "ben_h": 'Weniger klicken. <span class="hl">Mehr veröffentlichen.</span>',
    "b1_t": "Ein Klick statt zwanzig Runden", "b1_p": "Zwanzig Artikel heißen nicht mehr zwanzigmal kopieren, einfügen, Bilder hochladen, Links reparieren. Ordner hinzufügen, hochladen.",
    "b2_t": "Erst mal als Entwurf", "b2_p": "Alles kann als Entwurf ankommen. In WordPress prüfen und veröffentlichen, wenn es passt.",
    "b3_t": "Dein Text bleibt deiner", "b3_p": "Die Markdown-Dateien auf deiner Festplatte bleiben das Original, lesbar in jedem Editor, heute und in zehn Jahren.",
    "b4_t": "Gemacht für KI-Workflows", "b4_p": "Texte aus ChatGPT, Claude und Co. kommen ohnehin als Markdown. AutoPress bringt sie ohne Umwege auf deine Website.",
    "b5_t": "Auch für ganze Websites", "b5_p": "Umzug oder Neustart? Seiten und Beiträge gehen in einem Durchgang hoch, samt Schlagwörtern und Kategorien.",
    "sis_t": "Vom Macher von Hybrid", "sis_p": "Hybrid ist der Markdown-Editor, der weiß, wer was geschrieben hat: du, eine KI oder eine Quelle. AutoPress bringt, was du dort schreibst, zu WordPress.",
    "sis_link": "Hybrid entdecken",

    "end_h": 'In Markdown schreiben. <span class="hl">Im Stapel veröffentlichen.</span>',
    "end_lede": "Hybrid AutoPress kommt in den App Store: eine App für iPhone, iPad und Mac.",
    "req": "Benötigt iOS 17, iPadOS 17 oder macOS 14 · Englisch und Deutsch",
    "foot_imprint": "Impressum", "foot_privacy": "Datenschutz", "foot_hybrid": "Hybrid Editor",
    "foot_imprint_href": "../impressum/", "foot_privacy_href": "../datenschutz/",
    "foot_hybrid_href": "https://hybrid-editor.com/de/",
    "fine": "WordPress ist eine Marke der WordPress Foundation. Hybrid AutoPress ist eine unabhängige App und steht in keiner Verbindung zur WordPress Foundation, zu Automattic oder zu den genannten Hosting-Anbietern. Apple, iPhone, iPad, Mac und App Store sind Marken von Apple Inc. Die Screenshots zeigen Beispielinhalte; die Oberfläche der App gibt es auf Deutsch und Englisch.",
})


def build(strings):
    page = (HERE / "template.html").read_text(encoding="utf-8")
    values = dict(strings, site=SITE, canonical=SITE + strings["path"])

    def fill(match):
        key = match.group(1)
        if key not in values:
            raise KeyError(f"template asks for {key!r}, which {strings['lang']} does not have")
        return values[key]

    target = HERE / strings["path"] / "index.html"
    target.parent.mkdir(exist_ok=True)
    target.write_text(re.sub(r"\{\{(\w+)\}\}", fill, page), encoding="utf-8")
    print("wrote", target.relative_to(HERE))


for language in (EN, DE):
    build(language)
