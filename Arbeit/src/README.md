Dieses in Python3 geschriebene Programm implementiert Bildkompressionsverfahren, welche in der Seminararbeit vorgestellt werden.

# Installation

```
$ pip3 install -r requirements.txt
```

# Verwendung

Die Transformation in die YCrCb Darstellung, sowie die RLE werden immer angewendet. Mittels des Switches `-s` kann Chroma Subsampling aktiviert werden. Die Option `-q` in Kombination mit `-m [Quantisierungsfaktor]` aktiviert Quantisierung mit dem angegebenen Quantisierungsfaktor. Ohne Angabe des Quantisierungsfaktors wird eine Wert von 1 als Standardeinstellung angenommen. Beispiel mit Subsampling und maximalem Quantisierungsfaktor:

```
$ python3 ./encode_decode.py -s -q 31
```

Das zuerst angezeigte Bild ist das Originalbild. Nach dem Schließen des Anzeigefensters wird der Komprimierungs- und Dekomprimierungsprozess gestartet. Das Resultat wird im Anschluss angezeigt.
