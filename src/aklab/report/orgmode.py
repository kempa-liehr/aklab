from contexere.scheme import abbreviate_date
def batched(iterable, n=2):
    rows = int(len(iterable) / n)
    remainder = len(iterable) % n
    for i in range(rows):
        yield iterable[i * n:(i + 1) * n]
    if remainder > 0:
        yield iterable[-n:]

class Orgmode:
    def __init__(self, relfigpath=''):
        self.figpath = relfigpath

    def copyrightbox(self, *filenames, label=None,
                     caption="Put figure caption here."):
        if label is None:
            label = abbreviate_date(local=True) + 'a'
        if len(filenames) == 1:
            return self.standalone_figure(filenames[0], label=label, caption=caption)
        else:
            return self.multi_figure(*filenames, label=label, caption=caption)

    def standalone_figure(self, filename, label=None,
                          caption="Put figure caption here."):
        if label is None:
            label = abbreviate_date(local=True) + 'a'
        panel = ord('a')

        text = "#+BEGIN_export latex\n\\begin{figure}\n\\begin{center}\n"
        text += "\\copyrightbox[b]\n{\n\\includegraphics[width = 0.5\\textwidth]{" + self.figpath + filename + "}\n}\n"
        text += "{\\texttt{" + filename.replace('_', '\\_') + "}}\n"
        text += "\\end{center}\n\\caption{" + caption + "}\n\\label{fig:" + label + "}\n\\end{figure}\n#+END_export"
        print(text)
        return text

    def multi_figure(self, *filenames, label=None,
                     caption="Put figure caption here."):
        if label is None:
            label = abbreviate_date(local=True) + 'a'
        panel = ord('a')

        text = "#+BEGIN_export latex\n\\begin{figure}\n\\begin{tabular}{ll}\n"
        for two_filenames in batched(filenames):
            text += f"({chr(panel)})&({chr(panel + 1)})\\\\"
            first = True
            for fn in two_filenames:
                text += "\\copyrightbox[b]\n{\n\\includegraphics[width = 0.5\\textwidth]{" + self.figpath + fn + "}\n}\n"
                text += "{\\texttt{" + fn.replace('_', '\\_') + "}}\n"
                if first:
                    text += "&\n"
                first = ~first
            text += "\\end{tabular}\n\\caption{" + caption + "}\n\\label{fig:" + label + "}\n\\end{figure}\n#+END_export"
            panel += 2
        print(text)
        return text