document.addEventListener("DOMContentLoaded", function () {
    function initializeQuill(selector) {
        const quillContainer = document.querySelector(selector);
        if (!quillContainer) return;
    
        // Evita reinicialização se já existir um Quill dentro do container
        if (quillContainer.__quill) return;
    
        const textarea = document.querySelector(`[name="${quillContainer.dataset.target}"]`);
        if (!textarea) return;
    
        // Inicializa o editor Quill
        const quill = new Quill(selector, {
            theme: 'snow',
            modules: {
                toolbar: quillContainer.dataset.toolbar !== "false" ? [
                    [{ header: [1, 2, 3, 4, 5, 6, false] }],
                    [{ font: [] }],
                    [{ size: [] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    [{ color: [] }, { background: [] }],
                    [{ script: 'sub' }, { script: 'super' }],
                    [{ list: 'ordered' }, { list: 'bullet' }, { list: 'check' }],
                    [{ indent: '-1' }, { indent: '+1' }],
                    [{ direction: 'rtl' }],
                    [{ align: [] }],
                    ['blockquote', 'code-block'],
                    ['link'],
                    ['clean']
                ] : false,
                clipboard: { matchVisual: false },
                history: { delay: 1000, maxStack: 500, userOnly: true },
                syntax: true, // Suporte a highlight.js
            },
            placeholder: 'Digite seu texto aqui...',
            readOnly: false
        });
    
        // Armazena a instância no elemento para evitar reexecuções
        quillContainer.__quill = quill;
    
        quillContainer.style.height = '400px';
    
        if (textarea.value.trim() !== "") {
            quill.root.innerHTML = textarea.value;
        }
    
        quill.on('text-change', function () {
            textarea.value = quill.root.innerHTML;
        });
    
        document.querySelector('form').onsubmit = function () {
            textarea.value = quill.root.innerHTML;
        };
    }    

    // Inicializa todos os editores na página
    document.querySelectorAll('.quill-editor').forEach(function (editor) {
        initializeQuill(`#${editor.id}`);
    });
});
