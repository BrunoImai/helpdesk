# VIDEOAULA 2 — Consultas no `mongosh` (ou na aba "Shell" do Atlas)

```javascript
use helpdesk                              // seleciona (ou cria) o banco

// Inserir
db.tickets.insertOne({
  titulo: "VPN não conecta",
  descricao: "Desde ontem a VPN retorna erro 809.",
  prioridade: "alta",
  status: "aberto",
  tags: ["vpn", "rede"],
  mensagens: [{ autor: "ana@empresa.com", texto: "Não conecto.", enviada_em: new Date() }],
  criado_em: new Date()
})

// Ler
db.tickets.find()                                     // todos
db.tickets.find({ status: "aberto" })                 // filtro
db.tickets.find({ prioridade: "alta" }, { titulo: 1 }) // projeção (só o título)
db.tickets.find({ tags: "vpn" })                      // procura dentro de listas
db.tickets.find().sort({ criado_em: -1 }).limit(5)

// Atualizar
db.tickets.updateOne({ titulo: "VPN não conecta" }, { $set: { status: "resolvido" } })
db.tickets.updateOne({ titulo: "VPN não conecta" },
                     { $push: { mensagens: { autor: "suporte", texto: "Resolvido!", enviada_em: new Date() } } })

// Apagar
db.tickets.deleteOne({ status: "cancelado" })

// Contar e agrupar
db.tickets.countDocuments({ status: "aberto" })
db.tickets.aggregate([{ $group: { _id: "$status", total: { $sum: 1 } } }])
```

> Dica: o `_id` é gerado automaticamente (`ObjectId`) e contém a data de criação.
