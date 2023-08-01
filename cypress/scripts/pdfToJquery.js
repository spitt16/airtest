


function pdfToJquery(pdfDataBuffer) {
    return pdfjsLib.getDocument({data: pdfDataBuffer}).promise
        .then((pdf) => pdf.getPage(1))
        .then((page) => page.getTextContent())
        .then((textContent) => {
            const $div = $('<div>');
            textContent.items.forEach((item) => {
                const $span = $('<span>').text(item.str);
                $div.append($span);
            });
            return $div;
        });
}