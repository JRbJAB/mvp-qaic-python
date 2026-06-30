# 🧭 Runbook — Chat & Dev Delivery Rules 0.7.3

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS  
> **Version :** `CHAT_DEV_DELIVERY_RULES_0.7.3`  
> **Date :** 2026-06-20

---

## 1. Règle anti-troncature

```text
Si un contenu complet dépasse une réponse confortable :
- ne pas le coller intégralement dans le chat ;
- générer un fichier .md ou un ZIP ;
- donner un résumé court + lien ;
- vérifier que le fichier contient tout.
```

---

## 2. Règle scripts

```text
Pas de script tronqué.
Pas de bloc PowerShell/Python/Apps Script coupé.
Pas de placeholder si on connaît le chemin.
Si script long : ZIP + README + SHA256.
```

---

## 3. Règle documents

```text
Pas de fausse fusion.
Une vraie fusion = contenu source complet préservé + patch intégré.
Si plusieurs docs : pack unique.
Si docs historiques : conservation + supersede explicite.
```

---

## 4. Règle batch

```text
Batch Maxi +++ only.
Mode Fast & Fuse.
Pas de micro-batchs sauf urgence de sécurité.
```

---

## 5. Règle finale de message

Chaque réponse de livraison doit contenir :

```text
STATUS
CE QUI EST FAIT
CE QUI N'A PAS ÉTÉ FAIT
LIENS / EMPLACEMENTS
NEXT ACTION
```
