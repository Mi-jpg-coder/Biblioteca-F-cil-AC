const form = document.getElementById("form-livro");

const mensagem = document.getElementById("mensagem");

const lista = document.getElementById("lista-livros");

 

async function carregarLivros() {

 const resposta = await fetch("/livros");

 const livros = await resposta.json();

 

 lista.innerHTML = "";

 

 livros.forEach((livro) => {

   const item = document.createElement("li");

   item.textContent = `${livro.titulo} — ${livro.autor}${livro.ano ? ` (${livro.ano})` : ""}`;

   lista.appendChild(item);

 });

}

 

form.addEventListener("submit", async (evento) => {

 evento.preventDefault();

 
 const titulo = document.getElementById("titulo").value.trim();

 const autor = document.getElementById("autor").value.trim();

 const ano = document.getElementById("ano").value;

 
 const resposta = await fetch("/livros", {

   method: "POST",

   headers: { "Content-Type": "application/json" },

   body: JSON.stringify({ titulo, autor, ano })

 });

 

 const dados = await resposta.json();

 

 if (!resposta.ok) {

   mensagem.textContent = dados.erro;

   return;
 }

 mensagem.textContent = "Livro cadastrado com sucesso!";

 form.reset();

 await carregarLivros();

});

carregarLivros();