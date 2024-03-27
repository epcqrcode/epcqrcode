# Dependencies
- ImageMagick (`imagemagick`)
- Python3 (with libraries `pillow`, `pyzbar`)

# Usage
1. Install the dependencies, e.g. with.
```python
python3 -m venv venv && venv/bin/pip install -r requirements.txt
```

2. Run the script on the test cases.

```
venv/bin/python3 test.py <test_dir> (filename)
```
(The optional argument 'filename' can be used to only run specific tests)

# Examples

```tex
%TEST 0
%BCD
%002
%1
%SCT
%
%Wikimedia Foerdergesellschaft
%DE33100205000001194700
%EUR123.45
%
%
%
%

\documentclass{standalone}
\usepackage{../../epcqrcode}

\begin{document}

\qrset{height=10cm}%
\epcqr{
    name=Wikimedia Foerdergesellschaft,
    iban=DE33100205000001194700,
    amount=123.45,
}

\end{document}
```

```tex
%TEST 1
%No name provided

\documentclass{standalone}
\usepackage{../../epcqrcode}

\begin{document}

\qrset{height=10cm}%
\epcqr{
    charset=2,
    iban=DE33100205000001194700,
    amount=123.45,
}

\end{document}
```
