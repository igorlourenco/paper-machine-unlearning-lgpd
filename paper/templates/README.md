# Migração para o modelo do veículo

O `main.tex` concentra todo o preâmbulo; as seções em `sections/` usam apenas
comandos genéricos (`\section`, `\cite`/`\textcite`/`\parencite`, `\todo`,
ambientes `table`/`tabularx`). Trocar de veículo é, em regra, trocar o
preâmbulo. Nenhum modelo é versionado aqui; baixe-os na hora da migração.

## Estado atual

`main.tex` já usa `abntex2` (opção B abaixo), alvo: periódico jurídico
brasileiro / CONPEDI. A opção A fica como plano B.

## Opção A — SBC (WICS / CSBC)

Modelo oficial: https://www.sbc.org.br/documentos-da-sbc/ (buscar "modelo para
publicação de artigos"). Vem como `sbc-template.sty` + `sbc.bst` + exemplo.

1. Copiar `sbc-template.sty` e `sbc.bst` para `paper/`.
2. Em `main.tex`: `\documentclass[12pt]{article}` + `\usepackage{sbc-template}`;
   remover `geometry`, `setspace`, `microtype` (o `.sty` controla layout).
3. Remover `biblatex`/`csquotes` e `\addbibresource`. O modelo SBC usa BibTeX
   com `sbc.bst`: `\bibliographystyle{sbc}` e `\bibliography{references}` no
   lugar de `\printbibliography`.
4. Substituir citações: `\parencite{x}` → `\cite{x}`; `\textcite{x}` →
   `\citeonline{x}` (o `sbc.bst` fornece `\citeonline`). Buscar com
   `grep -rn "cite" paper/sections`.
5. Entradas `@legislation`/`@jurisdiction` em `references.bib` não são
   reconhecidas por BibTeX puro: converter para `@misc` com `howpublished`.
6. Em `.latexmkrc`, trocar `$bibtex_use = 2` e remover `$biber` (latexmk usa
   BibTeX por padrão quando encontra `\bibliography`).
7. Título, autores e `\address` conforme o exemplo do modelo; resumo em
   inglês (`abstract`) e português (`resumo`) nos ambientes do modelo.
8. Limites de página do WICS: conferir chamada de trabalhos do ano.

## Opção B — ABNT / abnTeX2 (periódicos jurídicos, CONPEDI)

Pacote `abntex2`. **Não vem no BasicTeX**; instalar sem sudo com
`tlmgr init-usertree && tlmgr --usermode install abntex2` (vai para
`~/Library/texmf`). TeX Live completo (CI) já o inclui. Para artigo
científico usar `\documentclass[article,12pt,oneside,a4paper,brazilian]{abntex2}`.

Já aplicado em `main.tex`: classe `abntex2`, `biblatex` com `style=abnt`
(**sem** `abntex2cite`), metadados via `\titulo`/`\autor`/`\local`/`\data`,
`\begin{resumo}` e `\begin{resumo}[Abstract]`, `\textual`/`\postextual`,
`\hypersetup` (a classe já carrega `hyperref`; não carregar de novo).

Ao escolher o periódico:

1. Conferir fonte, tamanho, limite de páginas e exigência de anonimização
   para revisão cega; ajustar só `main.tex`.
2. Conferir se o periódico exige "REFERÊNCIAS" em caixa alta (opção `title`
   de `\printbibliography`).
3. Se o periódico fornecer `.docx` em vez de LaTeX, gerar o PDF com abnTeX2 e
   verificar conformidade visual; alguns aceitam PDF direto.

## Checklist comum às duas opções

- [ ] `make pdf` compila sem erros.
- [ ] Todos os `\todo{}` removidos ou `\todo` redefinido como vazio.
- [ ] Todos os `% TODO: verificar` de `references.bib` resolvidos.
- [ ] `paper/tables/crosswalk.tex` regenerado a partir do CSV final.
- [ ] Workflow de CI ajustado se a cadeia biber → bibtex mudar.
