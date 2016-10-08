Hier vielleicht einmal eine kleine Zusammenstellung von Tools die wir benutzen (können) und einige Gedanken dazu:

# Drafting
* [Etherpads](https://pad.riseup.net/) - Haben den Vorteil, dass weniger Merge Conflicts auftreten, wenn wir beide beginnen unsere Ideen aufzuschreiben
* [epad-saver.py](https://github.com/importantchoice/epad-saver) - Habe ich gestern einmal zusammen gehackt, um dumps unserer Etherpads zu machen.

# Ideensammlung

* Einfache text-Dateien: Zum Ideen aufschreiben und kurz notieren reichen die vermutlich ganz gut aus. Schön daran ist, dass kein großes Tool gestartet werden muss, syncing mit git ist top. Wenn wir markdown benutzen ist auch Formatierung und strukturierung ohne großen Aufwand möglich. Dafür gibts bei github ja auch einen extra Editor.

# Quellenverwaltung

Probleme bei Quellenverwaltung:

1. Binary dumps (Bilder, zip-Archive etc.) sind für git doof, da nicht über diff effizient speicherbar
2. Vom Workflow her sollte möglichst beim Finden einer Quelle ein dump mit Access-Date und dump erstellt werden.
3. Bei Verwendung von git wären zusätzliche Schritte notwendig und ein push sollte nicht vergessen werden.
4. Syncing ist ein muss. Eigentlich wäre es aber schön dabei zusätzliche externe Services zu vermeiden.

* [Zotero](https://www.zotero.org) - Kann syncing (allerdings nur über deren Server), dumping, integriert sich mittels addon gut in den browser. Zusätzliche Notizen und tags zu Einträgen möglich. Export zu Biblatex möglich -> später weniger Arbeit.

	* Wir könnten auch unser eigenes Tool schreiben, welches git pull/push abnimmt. Anforderungen wären: Url geben -> Rekursives dumping und anschließendes zipping, Möglichst jede Quelle in eigene Datei, damit merge conflicts möglichst vermieden werden. Vorteil wäre, dass wir sync-technisch kein weiteres Tool bräuchten.

# Zeitplanung

Ideen:
* Einfache ToDo Liste: + Wenig verwaltungsaufwand, - Je nach Realisierung fallen nicht unbedingt Charts etc. dabei heraus
	* Über einfache text-Dateien könnten wir das gut über git syncen. Gibt es da bereits schon Tools für?
	* Ansonsten nutzen bereits existierende Programme gerne nur eine Datei zum speichern, was bei merge conflicts ziemlich nervig wird...
* ProjectLibre: + Gant Diagramme, + Direkt lernen mit professioneller Software zu arbeiten, - Java, - Wie syncen?, - Overkill?
