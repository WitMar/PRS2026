"""
Konwersja notatnika Jupyter do strony HTML w stylu pozostałych materiałów
(template.html + style.css, tak jak rst2html5.py w kompilacja.txt).

Użycie:
    python ipynb2html.py Zajecia1Jupyter.ipynb [--title "Laboratorium 1 - ..."]

Wymaga: nbconvert, docutils, pandoc.
Obrazki (załączniki z komórek markdown i wykresy z wyników) są wbudowywane w plik HTML (data URI),
więc wynikowa strona jest jednym samodzielnym plikiem.
"""
import argparse
import base64
import mimetypes
import os
import re

import nbformat
from docutils.core import publish_file
from nbconvert import RSTExporter
from traitlets.config import Config


def przygotuj_markdown(nb):
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue
        s = cell.source
        # <code>...</code> -> `...` (pandoc gubi surowy HTML przy konwersji do RST)
        s = re.sub(r"<code>(.*?)</code>", lambda m: "`" + m.group(1).replace("`", "") + "`", s)
        # "> Zrób to sam!\n>> ..." - zagnieżdżony cytat, który Jupyter renderuje inaczej niż pandoc
        s = re.sub(r"^>>[ ]?", "> ", s, flags=re.M)
        s = re.sub(r"^> (Zrób to sam!)[ ]*$", r"> **\1**\n>", s, flags=re.M)
        cell.source = s
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.metadata.pop("tags", None)


def popraw_rst(rst, obrazki):
    # .. figure:: + podpis "Screenshot from ..." -> wyśrodkowany obrazek bez podpisu
    rst = re.sub(r"\.\. figure:: (\S+)\n   :alt: (.*)\n\n   .*\n",
                 lambda m: f".. image:: {obrazki[m.group(1)]}\n   :align: center\n   :alt: {m.group(2)}\n",
                 rst)
    rst = re.sub(r"\.\. image:: (\S+)\n",
                 lambda m: f".. image:: {obrazki.get(m.group(1), m.group(1))}\n   :align: center\n", rst)
    rst = rst.replace("\n   :align: center\n   :align: center\n", "\n   :align: center\n")
    rst = rst.replace(".. code:: ipython3", ".. code:: python")
    # akapity "**Uwaga!** ..." w ramce jak w pozostałych materiałach
    rst = re.sub(r"\n\n(\*\*Uwaga!\*\*)", r"\n\n.. class:: important\n\n\1", rst)
    return rst


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook")
    parser.add_argument("--title", help="tytuł strony umieszczany nad treścią notatnika")
    args = parser.parse_args()

    nazwa = os.path.splitext(os.path.basename(args.notebook))[0]

    nb = nbformat.read(args.notebook, as_version=4)
    przygotuj_markdown(nb)

    cfg = Config()
    cfg.ExtractAttachmentsPreprocessor.enabled = True
    rst, zasoby = RSTExporter(config=cfg).from_notebook_node(nb)

    # docutils potrzebuje nazw plików - podstawiamy znaczniki, które po konwersji zamienimy na data URI
    obrazki, dane_obrazkow = {}, {}
    for nr, (plik, dane) in enumerate(zasoby["outputs"].items(), start=1):
        znacznik = f"obrazek-{nr:02d}{os.path.splitext(plik)[1]}"
        obrazki[plik] = znacznik
        typ = mimetypes.guess_type(plik)[0] or "image/png"
        dane_obrazkow[znacznik] = f"data:{typ};base64,{base64.b64encode(dane).decode('ascii')}"

    rst = popraw_rst(rst, obrazki)
    if args.title:
        rst = f"{args.title}\n{'=' * len(args.title)}\n\n{rst}"

    plik_rst = f"{nazwa}.rst"
    with open(plik_rst, "w", encoding="utf-8") as f:
        f.write(rst)

    publish_file(source_path=plik_rst, destination_path=f"{nazwa}.html", writer_name="html5",
                 settings_overrides={
                     "template": "template.html",
                     "stylesheet_path": "style.css",
                     "embed_stylesheet": False,
                     "cloak_email_addresses": True,
                     "doctitle_xform": False,
                     "math_output": "mathjax",
                     "title": args.title or nazwa,
                     "input_encoding": "utf-8",
                     "output_encoding": "utf-8",
                 })
    os.remove(plik_rst)

    with open(f"{nazwa}.html", encoding="utf-8") as f:
        html = f.read()
    html = re.sub(r'alt="obrazek-\d+\.\w+"', 'alt="wykres"', html)
    for znacznik, uri in dane_obrazkow.items():
        html = html.replace(f'src="{znacznik}"', f'src="{uri}"')
    with open(f"{nazwa}.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Zapisano {nazwa}.html ({len(dane_obrazkow)} obrazków wbudowanych w plik)")


if __name__ == "__main__":
    main()
