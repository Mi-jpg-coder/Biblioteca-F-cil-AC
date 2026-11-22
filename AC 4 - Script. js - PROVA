const formulario = document.getElementById("formLivro");
const campoTitulo = document.getElementById("titulo");
const campoAutor = document.getElementById("autor");
const campoAno = document.getElementById("ano");
const lista = document.getElementById("listaLivros");
const totalLivros = document.getElementById("totalLivros");
const mensagem = document.getElementById("mensagem");

const tituloFormulario = document.getElementById("tituloFormulario");
const descricaoFormulario = document.getElementById("descricaoFormulario");
const botaoSalvar = document.getElementById("botaoSalvar");
const botaoCancelar = document.getElementById("botaoCancelar");

let idEmEdicao = null;


formulario.addEventListener("submit", async function(evento) {
    evento.preventDefault();

    const dadosLivro = {
        titulo: campoTitulo.value.trim(),
        autor: campoAutor.value.trim(),
        ano: campoAno.value.trim() || null
    };

    if (!dadosLivro.titulo || !dadosLivro.autor) {
        mostrarMensagem("Preencha o título e o autor.", true);
        return;
    }

    const editando = idEmEdicao !== null;
    const url = editando ? `/livros/${idEmEdicao}` : "/livros";
    const metodo = editando ? "PUT" : "POST";

    try {
        const resposta = await fetch(url, {
            method: metodo,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dadosLivro)
        });

        const resultado = await resposta.json();

        if (!resposta.ok) {
            mostrarMensagem(resultado.erro || "Erro ao salvar livro.", true);
            return;
        }

        mostrarMensagem(
            editando
                ? "Livro atualizado com sucesso!"
                : "Livro cadastrado com sucesso!"
        );

        limparFormulario();
        await carregarLivros();

    } catch (erro) {
        mostrarMensagem(
            "Erro de conexão. Confira se o servidor está funcionando.",
            true
        );
    }
});


function mostrarMensagem(texto, erro = false) {
    mensagem.textContent = texto;
    mensagem.classList.toggle("mensagem-erro", erro);
}


function limparFormulario() {
    formulario.reset();
    idEmEdicao = null;

    tituloFormulario.textContent = "Cadastrar novo livro";
    descricaoFormulario.textContent =
        "Preencha as informações abaixo para adicionar um livro à sua biblioteca.";

    botaoSalvar.textContent = "📚 Cadastrar livro";
    botaoCancelar.hidden = true;
}


botaoCancelar.addEventListener("click", function() {
    limparFormulario();
    mostrarMensagem("Edição cancelada.");
});


async function carregarLivros() {
    try {
        const resposta = await fetch("/livros");
        const livros = await resposta.json();

        if (!resposta.ok) {
            throw new Error("Erro ao carregar livros.");
        }

        lista.innerHTML = "";
        totalLivros.textContent = livros.length;

        if (livros.length === 0) {
            const vazio = document.createElement("li");
            vazio.className = "vazio";
            vazio.innerHTML = `
                <div>📚</div>
                <h4>Nenhum livro cadastrado</h4>
                <p>Cadastre seu primeiro livro acima.</p>
            `;
            lista.appendChild(vazio);
            return;
        }

        livros.forEach(function(livro) {
            const item = document.createElement("li");
            item.className = "livro-item";

            const capa = document.createElement("div");
            capa.className = "capa";
            capa.textContent = "📖";

            const informacoes = document.createElement("div");
            informacoes.className = "informacoes";

            const titulo = document.createElement("h4");
            titulo.textContent = livro.titulo;

            const autor = document.createElement("p");
            autor.textContent = livro.autor;

            const ano = document.createElement("span");
            ano.className = "ano-livro";
            ano.textContent = "📅 " +
                (livro.ano ?? "Ano não informado");

            const acoes = document.createElement("div");
            acoes.className = "acoes-livro";

            const botaoEditar = document.createElement("button");
            botaoEditar.type = "button";
            botaoEditar.className = "btn-editar";
            botaoEditar.textContent = "✏️ Editar";

            botaoEditar.addEventListener("click", function() {
                iniciarEdicao(livro);
            });

            const botaoExcluir = document.createElement("button");
            botaoExcluir.type = "button";
            botaoExcluir.className = "btn-excluir";
            botaoExcluir.textContent = "🗑️ Excluir";

            botaoExcluir.addEventListener("click", function() {
                excluirLivro(livro.id, livro.titulo);
            });

            acoes.append(botaoEditar, botaoExcluir);
            informacoes.append(titulo, autor, ano, acoes);
            item.append(capa, informacoes);
            lista.appendChild(item);
        });

    } catch (erro) {
        mostrarMensagem(
            "Não foi possível carregar os livros. Confira o servidor e o MySQL.",
            true
        );
    }
}


function iniciarEdicao(livro) {
    idEmEdicao = livro.id;

    campoTitulo.value = livro.titulo;
    campoAutor.value = livro.autor;
    campoAno.value = livro.ano ?? "";

    tituloFormulario.textContent = "Editar livro";
    descricaoFormulario.textContent =
        "Altere as informações e clique em salvar.";

    botaoSalvar.textContent = "💾 Salvar alterações";
    botaoCancelar.hidden = false;
    mensagem.textContent = "";

    document.querySelector(".cadastro").scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

    campoTitulo.focus();
}


async function excluirLivro(id, titulo) {
    const confirmar = confirm(
        `Deseja realmente excluir o livro "${titulo}"?`
    );

    if (!confirmar) {
        return;
    }

    try {
        const resposta = await fetch(`/livros/${id}`, {
            method: "DELETE"
        });

        const resultado = await resposta.json();

        if (!resposta.ok) {
            mostrarMensagem(resultado.erro || "Erro ao excluir livro.", true);
            return;
        }

        if (idEmEdicao === id) {
            limparFormulario();
        }

        mostrarMensagem("Livro excluído com sucesso.");
        await carregarLivros();

    } catch (erro) {
        mostrarMensagem("Não foi possível conectar ao servidor.", true);
    }
}


carregarLivros();
