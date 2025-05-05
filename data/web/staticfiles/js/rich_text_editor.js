(function(){
    function createEditor(textarea) {
      // Oculta a textarea original
      textarea.style.display = 'none';
  
      // Cria o container principal do editor
      var container = document.createElement('div');
      container.className = 'rich-text-container';
  
      // Cria a toolbar
      var toolbar = document.createElement('div');
      toolbar.className = 'editor-toolbar';
  
      // Cria a área de edição
      var content = document.createElement('div');
      content.className = 'editor-content';
      content.contentEditable = true;
      content.innerHTML = textarea.value;
  
      // Força o foco de volta ao conteúdo se ele perder o foco para fora do container
      content.addEventListener('blur', function(){
        setTimeout(function(){
          if (!container.contains(document.activeElement)) {
            content.focus();
          }
        }, 0);
      });
  
      // Função utilitária para criar botões (com tabindex -1)
      function createButton(label, title, command, value, promptText) {
        var button = document.createElement('button');
        button.innerHTML = label;
        button.title = title;
        button.setAttribute('tabindex', '-1'); // evita que o botão receba foco
        button.onmousedown = function(e) {
          e.preventDefault(); // previne que o clique mude o foco
          if (promptText) {
            var url = window.prompt(promptText);
            if (url) {
              document.execCommand(command, false, url);
            }
          } else {
            document.execCommand(command, false, value || null);
          }
          // Reforça o foco de volta à área de edição
          setTimeout(function(){ content.focus(); }, 0);
          updateToolbarState();
        };
        return button;
      }
  
      // Função utilitária para criar selects (com tabindex -1)
      function createSelect(optionsArray, title, command) {
        var select = document.createElement('select');
        select.title = title;
        select.setAttribute('tabindex', '-1'); // evita foco
        optionsArray.forEach(function(optVal) {
          var opt = document.createElement('option');
          opt.value = optVal;
          opt.innerText = optVal;
          select.appendChild(opt);
        });
        select.onchange = function() {
          document.execCommand(command, false, this.value);
          setTimeout(function(){ content.focus(); }, 0);
          updateToolbarState();
        };
        return select;
      }
  
      // Criação dos controles
      var btnUndo         = createButton('↺', 'Desfazer', 'undo');
      var btnRedo         = createButton('↻', 'Refazer', 'redo');
      var btnRemoveFormat = createButton('Tx', 'Remover Formatação', 'removeFormat');
      var btnBold         = createButton('<b>B</b>', 'Negrito', 'bold');
      var btnItalic       = createButton('<i>I</i>', 'Itálico', 'italic');
      var btnUnderline    = createButton('<u>U</u>', 'Sublinhado', 'underline');
      var btnStrike       = createButton('<s>S</s>', 'Tachado', 'strikeThrough');
      var btnSubscript    = createButton('X₂', 'Subscrito', 'subscript');
      var btnSuperscript  = createButton('X²', 'Sobrescrito', 'superscript');
  
      var fontFamilies = ['Arial', 'Courier New', 'Georgia', 'Times New Roman', 'Verdana'];
      var selectFontFamily = createSelect(fontFamilies, 'Fonte', 'fontName');
  
      var fontSizes = [];
      for (var i = 1; i <= 7; i++){
        fontSizes.push(i);
      }
      var selectFontSize = createSelect(fontSizes, 'Tamanho da Fonte', 'fontSize');
  
      // Controles de cores (texto e fundo)
      var inputForeColor = document.createElement('input');
      inputForeColor.type = 'color';
      inputForeColor.title = 'Cor do Texto';
      inputForeColor.setAttribute('tabindex', '-1');
      inputForeColor.onchange = function() {
        document.execCommand('foreColor', false, this.value);
        setTimeout(function(){ content.focus(); }, 0);
        updateToolbarState();
      };
  
      var inputBackColor = document.createElement('input');
      inputBackColor.type = 'color';
      inputBackColor.title = 'Cor de Fundo';
      inputBackColor.setAttribute('tabindex', '-1');
      inputBackColor.onchange = function() {
        document.execCommand('hiliteColor', false, this.value);
        setTimeout(function(){ content.focus(); }, 0);
        updateToolbarState();
      };
  
      // Cria link e remove link
      var btnLink   = createButton('🔗', 'Criar Link', 'createLink', null, 'Digite a URL do link:');
      var btnUnlink = createButton('❌', 'Remover Link', 'unlink');
  
      // Alinhamento
      var btnAlignLeft   = createButton('≡', 'Alinhar à Esquerda', 'justifyLeft');
      var btnAlignCenter = createButton('≡', 'Centralizar', 'justifyCenter');
      var btnAlignRight  = createButton('≡', 'Alinhar à Direita', 'justifyRight');
      var btnJustify     = createButton('≡', 'Justificar', 'justifyFull');
  
      // Listas
      var btnOrderedList   = createButton('OL', 'Lista Ordenada', 'insertOrderedList');
      var btnUnorderedList = createButton('UL', 'Lista com Tópicos', 'insertUnorderedList');
  
      // Recuo
      var btnOutdent = createButton('←', 'Diminuir Recuo', 'outdent');
      var btnIndent  = createButton('→', 'Aumentar Recuo', 'indent');
  
      // Linha horizontal
      var btnHR = createButton('―', 'Linha Horizontal', 'insertHorizontalRule');
  
      // Adiciona os controles à toolbar
      toolbar.appendChild(btnUndo);
      toolbar.appendChild(btnRedo);
      toolbar.appendChild(btnRemoveFormat);
      toolbar.appendChild(btnBold);
      toolbar.appendChild(btnItalic);
      toolbar.appendChild(btnUnderline);
      toolbar.appendChild(btnStrike);
      toolbar.appendChild(btnSubscript);
      toolbar.appendChild(btnSuperscript);
      toolbar.appendChild(selectFontFamily);
      toolbar.appendChild(selectFontSize);
      toolbar.appendChild(inputForeColor);
      toolbar.appendChild(inputBackColor);
      toolbar.appendChild(btnLink);
      toolbar.appendChild(btnUnlink);
      toolbar.appendChild(btnAlignLeft);
      toolbar.appendChild(btnAlignCenter);
      toolbar.appendChild(btnAlignRight);
      toolbar.appendChild(btnJustify);
      toolbar.appendChild(btnOrderedList);
      toolbar.appendChild(btnUnorderedList);
      toolbar.appendChild(btnOutdent);
      toolbar.appendChild(btnIndent);
      toolbar.appendChild(btnHR);
  
      // Função que atualiza o estado dos controles da toolbar
      function updateToolbarState() {
        btnBold.classList.toggle('active', document.queryCommandState('bold'));
        btnItalic.classList.toggle('active', document.queryCommandState('italic'));
        btnUnderline.classList.toggle('active', document.queryCommandState('underline'));
        btnStrike.classList.toggle('active', document.queryCommandState('strikeThrough'));
        btnSubscript.classList.toggle('active', document.queryCommandState('subscript'));
        btnSuperscript.classList.toggle('active', document.queryCommandState('superscript'));
  
        var currentFont = document.queryCommandValue('fontName');
        if (currentFont) {
          currentFont = currentFont.replace(/['"]/g, '');
          for (var i = 0; i < selectFontFamily.options.length; i++) {
            if (selectFontFamily.options[i].value.toLowerCase() === currentFont.toLowerCase()) {
              selectFontFamily.selectedIndex = i;
              break;
            }
          }
        }
  
        var currentSize = document.queryCommandValue('fontSize');
        if (currentSize) {
          for (var i = 0; i < selectFontSize.options.length; i++) {
            if (selectFontSize.options[i].value == currentSize) {
              selectFontSize.selectedIndex = i;
              break;
            }
          }
        }
      }
  
      // Atualiza a textarea oculta e a toolbar conforme o conteúdo é alterado
      content.addEventListener('keyup', function(){
        textarea.value = content.innerHTML;
        updateToolbarState();
      });
      content.addEventListener('mouseup', updateToolbarState);
      content.addEventListener('click', updateToolbarState);
  
      // Previna que cliques na toolbar alterem o foco para fora do container
      container.addEventListener('mousedown', function(e) {
        if (!content.contains(e.target)) {
          e.preventDefault();
          setTimeout(function(){ content.focus(); }, 0);
        }
      });
  
      // Monta o editor e insere após a textarea
      container.appendChild(toolbar);
      container.appendChild(content);
      textarea.parentNode.insertBefore(container, textarea.nextSibling);
  
      // Foca o conteúdo ao inicializar
      content.focus();
    }
  
    // Inicializa o editor em todas as textareas com a classe "rich-text"
    document.addEventListener('DOMContentLoaded', function(){
      var textareas = document.querySelectorAll('textarea.rich-text');
      textareas.forEach(function(ta){
        createEditor(ta);
      });
    });
  })();
  