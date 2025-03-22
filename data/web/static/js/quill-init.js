document.addEventListener("DOMContentLoaded", function () {
    function initializeQuill(selector) {
        const quillContainer = document.querySelector(selector);
        if (!quillContainer) return;

        const textarea = document.querySelector(`[name="${quillContainer.dataset.target}"]`);
        if (!textarea) return;

        // Inicializa o editor Quill
        const quill = new Quill(selector, {
            theme: 'snow',
            modules: {
                toolbar: [
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
                ],
                clipboard: { matchVisual: false },
                history: { delay: 1000, maxStack: 500, userOnly: true },
                syntax: true, // Suporte a highlight.js
            },
            placeholder: 'Digite seu texto aqui...',
            readOnly: false
        });

        quillContainer.style.height = '400px';

        // Se o <textarea> já tem valor (exemplo: edição), carregá-lo no Quill
        if (textarea.value.trim() !== "") {
            quill.root.innerHTML = textarea.value;
        }

        // Atualiza o campo de texto real sempre que o Quill for alterado
        quill.on('text-change', function () {
            textarea.value = quill.root.innerHTML;
        });

        // Garante que o valor seja salvo no submit
        document.querySelector('form').onsubmit = function () {
            textarea.value = quill.root.innerHTML;
        };
    }

    // Inicializa todos os editores na página
    document.querySelectorAll('.quill-editor').forEach(function (editor) {
        initializeQuill(`#${editor.id}`);
    });
});
