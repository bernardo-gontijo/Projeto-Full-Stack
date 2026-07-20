// ================== LISTAR ==================
async function listarRegistros() {
  const resp = await fetch("/registros");
  const dados = await resp.json();
  renderizarTabela(dados);
}

// ================== RENDERIZAR TABELA ==================
function renderizarTabela(dados) {
  const corpo = document.getElementById("corpoTabela");
  corpo.innerHTML = "";

  dados.forEach((cliente) => {
    const linha = document.createElement("tr");

    linha.innerHTML = `
      <td>${cliente.id}</td>
      <td>${cliente.nome}</td>
      <td>${cliente.telefone}</td>
      <td>${cliente.unidade}</td>
      <td>${cliente.plano}</td>
      <td>${cliente.objetivo}</td>
      <td>${cliente.data_matricula}</td>
      <td>
        <button onclick="editarRegistro(${cliente.id})">Editar</button>
        <button onclick="deletarRegistro(${cliente.id})">Excluir</button>
      </td>
    `;

    corpo.appendChild(linha);
  });
}

// ================== CADASTRAR (chamado pelo botão do form) ==================
function cadastrarCliente() {
  const novoCliente = {
    nome: document.getElementById("nome").value,
    telefone: document.getElementById("telefone").value,
    unidade: document.getElementById("unidade").value,
    plano: document.getElementById("plano").value,
    objetivo: document.getElementById("objetivo").value,
    data_matricula: document.getElementById("data_matricula").value,
  };

  if (!novoCliente.nome || !novoCliente.telefone) {
    document.getElementById("mensagemCadastro").textContent =
      "Preencha ao menos Nome e Telefone.";
    return;
  }

  criarRegistro(novoCliente);
  document.getElementById("formCadastro").reset();
  document.getElementById("mensagemCadastro").textContent =
    "Cliente cadastrado com sucesso!";
}

// ================== CRIAR ==================
async function criarRegistro(novosDados) {
  await fetch("/registros", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(novosDados),
  });

  listarRegistros();
}

// ================== BUSCAR POR ID ==================
async function buscarPorId() {
  const id = document.getElementById("idBusca").value;
  const resultado = document.getElementById("resultadoBusca");

  if (!id) {
    resultado.textContent = "Digite um ID para buscar.";
    return;
  }

  const resp = await fetch(`/registros/${id}`);

  if (!resp.ok) {
    resultado.textContent = "Cliente não encontrado.";
    return;
  }

  const cliente = await resp.json();
  resultado.textContent =
    `ID: ${cliente.id} | Nome: ${cliente.nome} | Telefone: ${cliente.telefone} | ` +
    `Unidade: ${cliente.unidade} | Plano: ${cliente.plano} | Objetivo: ${cliente.objetivo} | ` +
    `Matrícula: ${cliente.data_matricula}`;
}

// ================== EDITAR ==================
async function editarRegistro(id) {
  // Busca os dados atuais para preencher os prompts
  const resp = await fetch(`/registros/${id}`);
  if (!resp.ok) return;
  const cliente = await resp.json();
  console.log(cliente); 

  const nome = prompt("Nome:", cliente.nome) ?? cliente.nome;
  const telefone = prompt("Telefone:", cliente.telefone) ?? cliente.telefone;
  const unidade = prompt("Unidade:", cliente.unidade) ?? cliente.unidade;
  const plano = prompt("Plano:", cliente.plano) ?? cliente.plano;
  const objetivo = prompt("Objetivo:", cliente.objetivo) ?? cliente.objetivo;
  const data_matricula = prompt("Data de Matrícula (AAAA-MM-DD):", cliente.data_matricula) ?? cliente.data_matricula;

  const dadosAtualizados = { nome, telefone, unidade, plano, objetivo, data_matricula };

  await fetch(`/registros/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dadosAtualizados),
  });

  listarRegistros();
}

// ================== DELETAR ==================
async function deletarRegistro(id) {
  const confirmar = confirm("Deseja realmente excluir este cliente?");
  if (!confirmar) return;

  await fetch(`/registros/${id}`, { method: "DELETE" });
  listarRegistros();
}

// ================== EXPORTAR CSV ==================
function exportarCSV() {
  window.location.href = "/exportar";
}

// ================== INICIALIZAÇÃO ==================
document.addEventListener("DOMContentLoaded", listarRegistros);