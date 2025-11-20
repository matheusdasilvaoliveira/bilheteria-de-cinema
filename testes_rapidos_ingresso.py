from modulos.ingresso.ingresso import listaIngressos, lista_ingressos_sessao, lista_ingressos_cliente

listaIngressos.clear()

listaIngressos.append({"id": 1, "cliente_id": 10, "sessao_id": 5, "numero_assento": 2, "preco": 20})
listaIngressos.append({"id": 2, "cliente_id": 10, "sessao_id": 5, "numero_assento": 3, "preco": 20})
listaIngressos.append({"id": 3, "cliente_id": 11, "sessao_id": 6, "numero_assento": 1, "preco": 20})

print("Ingressos sessão 5:")
print(lista_ingressos_sessao(5))

print("\nIngressos sessão 6:")
print(lista_ingressos_sessao(6))

print("\nIngressos cliente 10:")
print(lista_ingressos_cliente(10))

print("\nIngressos cliente 11:")
print(lista_ingressos_cliente(11))
