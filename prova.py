class No:
    def __init__(self, valor):
        self.esquerda = None
        self.valor = valor
        self.direita = None
        self.altura = 1

class ArvoreAVL:
    def __init__(self, raiz=None):
        self.raiz = raiz

    def vazia(self):
        return self.raiz is None

    def adicionar_no(self, valor):
        if self.vazia():
            self.raiz = No(valor)
        else:
            self.raiz = self._adicionar_no_folha(self.raiz, valor)

    def _adicionar_no_folha(self, no_atual, valor):
        if not no_atual:
            return No(valor)
        elif valor < no_atual.valor:
            no_atual.esquerda = self._adicionar_no_folha(no_atual.esquerda, valor)
        else:
            no_atual.direita = self._adicionar_no_folha(no_atual.direita, valor)

        no_atual.altura = 1 + max(self._altura(no_atual.esquerda), self._altura(no_atual.direita))
        balanceamento = self._balanceamento(no_atual)

        if balanceamento > 1:
            if valor < no_atual.esquerda.valor:
                return self._rotacao_direita(no_atual)
            else:
                no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda)
                return self._rotacao_direita(no_atual)

        if balanceamento < -1:
            if valor > no_atual.direita.valor:
                return self._rotacao_esquerda(no_atual)
            else:
                no_atual.direita = self._rotacao_direita(no_atual.direita)
                return self._rotacao_esquerda(no_atual)

        return no_atual

    def remover_no(self, valor):
        self.raiz = self._remover_no(self.raiz, valor)

    def _remover_no(self, no, valor):
        if not no:
            return no

        if valor < no.valor:
            no.esquerda = self._remover_no(no.esquerda, valor)
        elif valor > no.valor:
            no.direita = self._remover_no(no.direita, valor)
        else:
            if no.esquerda is None:
                temp = no.direita
                no = None
                return temp
            elif no.direita is None:
                temp = no.esquerda
                no = None
                return temp

            temp = self._get_min_value_node(no.direita)
            no.valor = temp.valor
            no.direita = self._remover_no(no.direita, temp.valor)

        if no is None:
            return no

        no.altura = 1 + max(self._altura(no.esquerda), self._altura(no.direita))
        balanceamento = self._balanceamento(no)

        if balanceamento > 1 and self._balanceamento(no.esquerda) >= 0:
            return self._rotacao_direita(no)

        if balanceamento > 1 and self._balanceamento(no.esquerda) < 0:
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)

        if balanceamento < -1 and self._balanceamento(no.direita) <= 0:
            return self._rotacao_esquerda(no)

        if balanceamento < -1 and self._balanceamento(no.direita) > 0:
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)

        return no

    def _get_min_value_node(self, no):
        if no is None or no.esquerda is None:
            return no
        return self._get_min_value_node(no.esquerda)

    def _altura(self, no):
        if not no:
            return 0
        return no.altura

    def _balanceamento(self, no):
        if not no:
            return 0
        return self._altura(no.esquerda) - self._altura(no.direita)

    def _rotacao_esquerda(self, pai):
        filhoD = pai.direita
        neto = filhoD.esquerda

        filhoD.esquerda = pai
        pai.direita = neto

        pai.altura = 1 + max(self._altura(pai.esquerda), self._altura(pai.direita))
        filhoD.altura = 1 + max(self._altura(filhoD.esquerda), self._altura(filhoD.direita))

        return filhoD

    def _rotacao_direita(self, pai):
        filhoE = pai.esquerda
        neto = filhoE.direita

        filhoE.direita = pai
        pai.esquerda = neto

        pai.altura = 1 + max(self._altura(pai.esquerda), self._altura(pai.direita))
        filhoE.altura = 1 + max(self._altura(filhoE.esquerda), self._altura(filhoE.direita))

        return filhoE

    def imprimir(self):
        if self.vazia():
            print("Árvore vazia")
            return
        self._imprimir(self.raiz)

    def _imprimir(self, no_atual):
        if no_atual is not None:
            self._imprimir(no_atual.esquerda)
            print(f"Nó: {no_atual.valor} - Altura: {no_atual.altura}")
            self._imprimir(no_atual.direita)

# Testando a árvore AVL
if __name__ == "__main__":
    arvore = ArvoreAVL()
    # Exemplo de adição e remoção de nós
    arvore.adicionar_no(10)
    arvore.adicionar_no(20)
    arvore.adicionar_no(30)
    arvore.adicionar_no(40)
    arvore.adicionar_no(50)
    arvore.adicionar_no(25)
    
    print("Árvore após adições:")
    arvore.imprimir()

    arvore.remover_no(30)
    print("\nÁrvore após a remoção do valor 30:")
    arvore.imprimir()
