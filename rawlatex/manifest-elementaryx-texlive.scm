;; Ce qui suit est un « manifeste » équivalent à la ligne de commande que vous
;; avez passée. Vous pouvez le sauvegarder dans un fichier qui vous pourrez
;; passer aux commandes « guix » qui acceptent l'option « --manifest »
;; (ou « -m »).

(specifications->manifest
  (list "texlive-scheme-basic"
        "texlive-soul"
        "texlive-todonotes"
        "texlive-tikz-timing"
        "texlive-wasysym"
        "texlive-wasy"
        "texlive-beamer"
        "python-pygments"
        "inkscape"
        "emacs-elementaryx-ox-beamer-minimal"))