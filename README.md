# pdf2epub
* requirements.txt
```
conda create -n pdf2epub python==3.10
conda activate pdf2epub
pip install pymupdf pdf2image pytesseract ebooklib
conda install -c conda-forge poppler (for macOS)
(https://brew.sh/zh-cn/)
brew install tesseract (for macOS)
```
* 这个脚本能够实现将图片版本的PDF转化为EPUB